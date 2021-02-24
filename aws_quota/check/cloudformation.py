from .quota_check import QuotaCheck, QuotaScope


class StackCountCheck(QuotaCheck):
    key = "cf_stack_count"
    description = "Cloud Formation Stack count"
    scope = QuotaScope.ACCOUNT
    service_code = 'cloudformation'
    quota_code = 'L-0485CB21'

    @property
    def current(self):
        return len(self.boto_session.client('cloudformation').list_stacks()['StackSummaries'])
