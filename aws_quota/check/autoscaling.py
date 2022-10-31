from .quota_check import QuotaCheck, QuotaScope, RegionQuotaCheck


class AutoScalingGroupCountCheck(RegionQuotaCheck):
    key = "asg_count"
    description = "Auto Scaling groups per Region"
    scope = QuotaScope.REGION
    service_code = 'autoscaling'
    quota_code = 'L-CDE20ADC'

    @property
    def current(self):
        return len(self.boto_session.client('autoscaling').describe_auto_scaling_groups()['AutoScalingGroups'])


class LaunchConfigurationCountCheck(RegionQuotaCheck):
    key = "lc_count"
    description = "Launch configurations per Region"
    scope = QuotaScope.REGION
    service_code = 'autoscaling'
    quota_code = 'L-6B80B8FA'

    @property
    def current(self):
        return len(self.boto_session.client('autoscaling').describe_launch_configurations()['LaunchConfigurations'])
