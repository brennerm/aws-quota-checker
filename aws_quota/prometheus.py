import asyncio
from aws_quota.exceptions import InstanceWithIdentifierNotFound
from aws_quota.utils import get_account_id
import dataclasses
import logging
import signal
import time
import contextlib
import typing

from aws_quota.check.quota_check import InstanceQuotaCheck, QuotaCheck

import boto3
import prometheus_client as prom

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class PrometheusExporterSettings:
    port: int
    namespace: str
    get_currents_interval: int
    get_limits_interval: int
    reload_checks_interval: int
    enable_duration_metrics: bool


class PrometheusExporter:
    def __init__(self,
                 session: boto3.Session,
                 check_classes: typing.List[QuotaCheck],
                 settings: PrometheusExporterSettings):
        self.session = session
        self.check_classes = check_classes
        self.checks = []
        self.settings = settings

        # unregister default collectors
        for name in list(prom.REGISTRY._names_to_collectors.values()):
            with contextlib.suppress(KeyError):
                prom.REGISTRY.unregister(name)

        prom.Info(f'{self.settings.namespace}', 'AWS quota checker info').info({
            **self.default_labels
        })

    @property
    def default_labels(self):
        return {
            'account': get_account_id(self.session),
            'region': self.session.region_name
        }

    @contextlib.contextmanager
    def timeit_gauge(self, prefix: str, labels: dict = None, **kwargs):
        if labels is None:
            labels = self.default_labels

        start = time.time()
        try:
            yield
        finally:
            duration = time.time() - start

            if self.settings.enable_duration_metrics:
                PrometheusExporter.get_or_create_gauge(
                    name=f'{prefix}_duration_seconds',
                    labelnames=labels.keys(),
                    **kwargs).labels(**labels).set(duration)

    @staticmethod
    def get_or_create_gauge(name, **kwargs) -> prom.Gauge:
        if name in prom.REGISTRY._names_to_collectors:
            return prom.REGISTRY._names_to_collectors[name]

        return prom.Gauge(name, **kwargs)

    def drop_obsolete_check(self):
        raise NotImplementedError

    async def load_checks_job(self):
        g = PrometheusExporter.get_or_create_gauge(
            f'{self.settings.namespace}_check_count',
            documentation='Number of AWS Quota Checks'
        )

        while True:
            with self.timeit_gauge(
                f'{self.settings.namespace}_collect_checks',
                documentation='Time to collect all quota checks'
            ):
                logger.info('collecting checks')
                checks = []
                for chk in self.check_classes:
                    try:
                        if issubclass(chk, InstanceQuotaCheck):
                            for identifier in chk.get_all_identifiers(self.session):
                                checks.append(
                                    chk(self.session, identifier)
                                )
                        else:
                            checks.append(chk(self.session))
                    except Exception:
                        logger.error('failed to collect check %s', chk)

                g.set(len(checks))
                self.checks = checks
                logger.info(f'collected {len(checks)} checks')
            await asyncio.sleep(self.settings.reload_checks_interval)

    async def get_limits_job(self):

        while True:
            with self.timeit_gauge(
                f'{self.settings.namespace}_check_limits',
                documentation='Time to check limits of all quotas'
            ):
                logger.info('refreshing limits')
                checks_to_drop = []

                for check in self.checks:
                    labels = check.label_values
                    name = f'{self.settings.namespace}_{check.key}_limit'

                    try:
                        with self.timeit_gauge(
                            name,
                            documentation=f'Time to collect {check.description} Limit'
                        ):
                            value = check.maximum

                        PrometheusExporter.get_or_create_gauge(
                            name,
                            documentation=f'{check.description} Limit',
                            labelnames=labels.keys()
                        ).labels(**check.label_values).set(value)
                    except InstanceWithIdentifierNotFound as e:
                        logger.warn(
                            'instance with identifier %s does not exist anymore, dropping it...', e.check.instance_id)
                        checks_to_drop.append(e.check)
                    except Exception:
                        logger.error(
                            'getting maximum of quota %s failed', check)

                for check in checks_to_drop:
                    self.checks.remove(check)

            logger.info('limits refreshed')
            await asyncio.sleep(self.settings.get_limits_interval)

    async def get_currents_job(self):

        while True:
            with self.timeit_gauge(
                f'{self.settings.namespace}_check_currents',
                documentation='Time to check limits of all quotas'
            ):

                logger.info('refreshing current values')
                checks_to_drop = []
                for check in self.checks:
                    labels = check.label_values
                    name = f'{self.settings.namespace}_{check.key}'

                    try:
                        with self.timeit_gauge(
                            name,
                            documentation=f'Time to collect {check.description}'
                        ):
                            value = check.current

                        PrometheusExporter.get_or_create_gauge(
                            name,
                            documentation=check.description,
                            labelnames=labels.keys()
                        ).labels(**check.label_values).set(value)
                    except InstanceWithIdentifierNotFound as e:
                        logger.warn(
                            'instance with identifier %s does not exist anymore, dropping it...', e.check.instance_id)
                        checks_to_drop.append(e.check)
                    except Exception:
                        logger.error(
                            'getting maximum of quota %s failed', check)

                for check in checks_to_drop:
                    self.checks.remove(check)

            logger.info('current values refreshed')
            await asyncio.sleep(self.settings.get_currents_interval)

    def serve(self):
        logger.info(f'starting /metrics endpoint on port {self.settings.port}')
        prom.start_http_server(self.settings.port)

    async def background_jobs(self):
        await asyncio.gather(
            self.load_checks_job(),
            self.get_limits_job(),
            self.get_currents_job(),
            return_exceptions=True
        )

    def start(self):
        self.serve()
        try:
            asyncio.run(self.background_jobs())
        except KeyboardInterrupt:
            logger.info('shutting down...')
