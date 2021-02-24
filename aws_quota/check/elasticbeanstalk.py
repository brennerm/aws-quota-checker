from .quota_check import QuotaCheck, QuotaScope


class ApplicationCountCheck(QuotaCheck):
    key = "elasticbeanstalk_application_count"
    description = "Elastic Beanstalk Applications per account"
    scope = QuotaScope.ACCOUNT
    service_code = 'elasticbeanstalk'
    quota_code = 'L-1CEABD17'

    @property
    def current(self):
        return len(self.boto_session.client('elasticbeanstalk').describe_applications()['Applications'])


class EnvironmentCountCheck(QuotaCheck):
    key = "elasticbeanstalk_environment_count"
    description = "Elastic Beanstalk Environments per account"
    scope = QuotaScope.ACCOUNT
    service_code = 'elasticbeanstalk'
    quota_code = 'L-8EFC1C51'

    @property
    def current(self):
        return len(self.boto_session.client('elasticbeanstalk').describe_environments()['Environments'])
