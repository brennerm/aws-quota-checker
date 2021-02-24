from .quota_check import QuotaCheck, QuotaScope


class AlarmCountCheck(QuotaCheck):
    key = "cw_alarm_count"
    description = "Number of CloudWatch alarms per region"
    scope = QuotaScope.REGION
    service_code = 'monitoring'
    quota_code = 'L-2FF78D7B'

    @property
    def current(self):
        alarms = self.boto_session.client('cloudwatch').describe_alarms()
        return len(alarms['CompositeAlarms']) + len(alarms['MetricAlarms'])
