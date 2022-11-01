from .quota_check import RegionQuotaCheck, QuotaScope


class TopicCountCheck(RegionQuotaCheck):
    key = "ses_daily_sends"
    description = "SES messages sent during the last 24 hours"
    scope = QuotaScope.REGION
    service_code = 'ses'
    quota_code = 'L-804C8AE8'

    @property
    def current(self):
        return self.boto_session.client('ses').get_send_quota()['SentLast24Hours']
