import logging
from aws_quota.utils import get_account_id
import enum
import typing
import sys
import boto3
import click
import tabulate

from aws_quota.check.quota_check import InstanceQuotaCheck, QuotaCheck, QuotaScope
from aws_quota.check import ALL_CHECKS, ALL_INSTANCE_SCOPED_CHECKS

CHECKMARK = u'\u2713'
ALL_CHECKS_CHOICE = click.Choice(['all'] + [chk.key for chk in ALL_CHECKS])


def check_keys_to_check_classes(check_string: str):
    split_check_keys = check_string.split(',')
    blacklisted_check_keys = []
    whitelisted_check_keys = []

    for key in split_check_keys:
        if key.startswith('!'):
            blacklisted_check_keys.append(key.lstrip('!'))
        else:
            whitelisted_check_keys.append(key)

    if 'all' in whitelisted_check_keys:
        selected_checks = ALL_CHECKS
    else:
        selected_checks = list(
            filter(lambda c: c.key in whitelisted_check_keys, ALL_CHECKS))

    return list(
        filter(lambda c: c.key not in blacklisted_check_keys, selected_checks))


class Runner:
    class ReportResult(enum.Enum):
        SUCCESS = 0
        WARNING = 1
        ERROR = 2

    def __init__(self, session: boto3.Session,
                 checks: typing.List[QuotaCheck],
                 warning_threshold: float,
                 error_threshold: float,
                 fail_on_error: bool) -> None:

        self.session = session
        self.checks = checks
        self.warning_threshold = warning_threshold
        self.error_threshold = error_threshold
        self.fail_on_warning = fail_on_error

    def __report(self, description, scope, current, maximum) -> ReportResult:
        if maximum != 0:
            percentage = (current / maximum)
        else:
            percentage = 0

        if percentage <= self.warning_threshold:
            symbol = CHECKMARK
            color = 'green'
            result = Runner.ReportResult.SUCCESS
        elif self.error_threshold >= percentage > self.warning_threshold:
            symbol = '!'
            color = 'yellow'
            result = Runner.ReportResult.WARNING
        else:
            symbol = 'X'
            color = 'red'
            result = Runner.ReportResult.ERROR

        click.echo(
            f'{description} [{scope}]: {current}/{maximum} ', nl=False)

        click.echo(click.style(symbol, fg=color, bold=True))

        return result

    def run_checks(self):
        errors = 0
        warnings = 0

        for chk in self.checks:
            current = chk.current
            maximum = chk.maximum

            if chk.scope == QuotaScope.ACCOUNT:
                scope = get_account_id(self.session)
            elif chk.scope == QuotaScope.REGION:
                scope = f'{get_account_id(self.session)}/{self.session.region_name}'
            elif chk.scope == QuotaScope.INSTANCE:
                scope = f'{get_account_id(self.session)}/{self.session.region_name}/{chk.instance_id}'

            result = self.__report(chk.description, scope, current, maximum)

            if result == Runner.ReportResult.WARNING:
                warnings += 1
            elif result == Runner.ReportResult.ERROR:
                errors += 1

        if (self.fail_on_warning and warnings > 0) or errors > 0:
            sys.exit(1)


@click.group()
def cli():
    pass


def common_scope_options(function):
    function = click.option(
        '--region', help='Region to use for region scoped quotas, defaults to current')(function)
    function = click.option(
        '--profile', help='AWS profile name to use, defaults to current')(function)

    return function


def common_check_options(function):
    function = click.option(
        '--warning-threshold', help='Warning threshold percentage for quota utilization, defaults to 0.8', default=0.8)(function)
    function = click.option(
        '--error-threshold', help='Error threshold percentage for quota utilization, defaults to 0.9', default=0.9)(function)
    function = click.option('--fail-on-warning/--no-fail-on-warning',
                            help='Exit with non-zero error code on quota warning, defaults to false', default=False)(function)

    return function


@cli.command()
@common_scope_options
@common_check_options
@click.argument('check-keys')
def check(check_keys, region, profile, warning_threshold, error_threshold, fail_on_warning):
    """Run checks identified by CHECK_KEYS

    e.g. check vpc_count,ecs_count

    Blacklist checks by prefixing them with !

    e.g. check all,!vpc_count

    Execute list-checks command to get available check keys

    Pass all to run all checks

    For instance checks it'll run through each individual instance available"""

    selected_checks = check_keys_to_check_classes(check_keys)

    session = boto3.Session(region_name=region, profile_name=profile)

    click.echo(
        f'AWS profile: {session.profile_name} | AWS region: {session.region_name} | Active checks: {",".join([check.key for check in selected_checks])}')

    checks = []

    with click.progressbar(selected_checks, label='Collecting checks', show_eta=False) as selected_checks:
        for chk in selected_checks:
            if issubclass(chk, InstanceQuotaCheck):
                for identifier in chk.get_all_identifiers(session):
                    checks.append(
                        chk(session, identifier)
                    )
            else:
                checks.append(chk(session))

    Runner(session, checks, warning_threshold,
           error_threshold, fail_on_warning).run_checks()


@cli.command()
@common_scope_options
@common_check_options
@click.argument('check-key', type=click.Choice([chk.key for chk in ALL_INSTANCE_SCOPED_CHECKS]))
@click.argument('instance-id')
def check_instance(check_key, instance_id, region, profile, warning_threshold, error_threshold, fail_on_warning):
    """Run single check for single instance

    e.g. check-instance vpc_acls_per_vpc vpc-0123456789

    Execute list-checks command to get available instance checks"""

    session = boto3.Session(region_name=region, profile_name=profile)

    selected_check = next(
        filter(lambda mon: mon.key == check_key, ALL_INSTANCE_SCOPED_CHECKS), None)

    click.echo(
        f'AWS profile: {session.profile_name} | AWS region: {session.region_name} | Active check: {selected_check.key} | Instance ID: {instance_id}')

    chk = selected_check(session, instance_id)

    Runner(session, [chk], warning_threshold,
           error_threshold, fail_on_warning).run_checks()


@cli.command()
@common_scope_options
@click.option('--port', help='Port on which to expose the Prometheus /metrics endpoint, defaults to 8080', default=8080)
@click.option('--namespace', help='Namespace/prefix for Prometheus metrics, defaults to awsquota', default='awsquota')
@click.option('--limits-check-interval', help='Interval in seconds at which to check the limit quota value, defaults to 600', default=600)
@click.option('--currents-check-interval', help='Interval in seconds at which to check the current quota value, defaults to 300', default=300)
@click.option('--reload-checks-interval', help='Interval in seconds at which to collect new checks e.g. when a new resource has been created, defaults to 600', default=600)
@click.option('--enable-duration-metrics/--disable-duration-metrics', help='Flag to control whether to collect/expose duration metrics, defaults to true', default=True)
@click.argument('check-keys')
def prometheus_exporter(check_keys, region, profile, port, namespace, limits_check_interval, currents_check_interval, reload_checks_interval, enable_duration_metrics):
    """Start a Prometheus exporter for quota checks

    Set checks to execute with CHECK_KEYS

    e.g. check vpc_count,ecs_count

    Blacklist checks by prefixing them with !

    e.g. check all,!vpc_count

    Execute list-checks command to get available check keys

    Pass all to run all checks
    """
    from aws_quota.prometheus import PrometheusExporter, PrometheusExporterSettings

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'
    )

    selected_checks = check_keys_to_check_classes(check_keys)

    session = boto3.Session(region_name=region, profile_name=profile)

    click.echo(
        f'AWS profile: {session.profile_name} | AWS region: {session.region_name} | Active checks: {",".join([check.key for check in selected_checks])}')

    settings = PrometheusExporterSettings(
        port=port,
        namespace=namespace,
        get_currents_interval=currents_check_interval,
        get_limits_interval=limits_check_interval,
        reload_checks_interval=reload_checks_interval,
        enable_duration_metrics=enable_duration_metrics
    )

    PrometheusExporter(session, selected_checks, settings).start()


@cli.command()
def list_checks():
    """List available quota checks"""
    click.echo(tabulate.tabulate([(chk.key, chk.description, chk.scope.name, getattr(chk, 'instance_id', 'N/A'))
                                  for chk in ALL_CHECKS], headers=['Key', 'Description', 'Scope', 'Instance ID']))


if __name__ == '__main__':
    cli()
