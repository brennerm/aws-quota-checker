from aws_quota.exceptions import InstanceWithIdentifierNotFound
import typing
import boto3
from .quota_check import QuotaCheck, InstanceQuotaCheck, QuotaScope


def get_albs(session: boto3.Session):
    return list(
        filter(
            lambda lb: lb['Type'] == 'application',
            session.client('elbv2').describe_load_balancers()['LoadBalancers'],
        )
    )


def get_nlbs(session: boto3.Session):
    return list(
        filter(
            lambda lb: lb['Type'] == 'network',
            session.client('elbv2').describe_load_balancers()['LoadBalancers'],
        )
    )


class ClassicLoadBalancerCountCheck(QuotaCheck):
    key = "elb_clb_count"
    description = "Classic Load Balancers per region"
    scope = QuotaScope.REGION
    service_code = 'elasticloadbalancing'
    quota_code = 'L-E9E9831D'

    @property
    def current(self):
        return len(
            self.boto_session.client('elb').describe_load_balancers()['LoadBalancerDescriptions']
        )


class ListenerPerClassicLoadBalancerCountCheck(InstanceQuotaCheck):
    key = "elb_listeners_per_clb"
    description = "Listeners per Classic Load Balancer"
    service_code = 'elasticloadbalancing'
    quota_code = 'L-1A491844'
    instance_id = 'Load Balancer Name'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [
            lb['LoadBalancerName']
            for lb in session.client('elb').describe_load_balancers()['LoadBalancerDescriptions']
        ]

    @property
    def current(self):
        try:
            return len(
                self.boto_session.client('elb').describe_load_balancers(
                    LoadBalancerNames=[self.instance_id]
                )['LoadBalancerDescriptions'][0]['ListenerDescriptions']
            )
        except self.boto_session.client('elb').exceptions.AccessPointNotFoundException as e:
            raise InstanceWithIdentifierNotFound(self) from e


class NetworkLoadBalancerCountCheck(QuotaCheck):
    key = "elb_nlb_count"
    description = "Network Load Balancers per region"
    scope = QuotaScope.REGION
    service_code = 'elasticloadbalancing'
    quota_code = 'L-69A177A2'

    @property
    def current(self):
        return len(
            list(
                filter(
                    lambda lb: lb['Type'] == 'network',
                    self.boto_session.client('elbv2').describe_load_balancers()['LoadBalancers'],
                )
            )
        )


class ListenerPerNetworkLoadBalancerCountCheck(InstanceQuotaCheck):
    key = "elb_listeners_per_nlb"
    description = "Listeners per Network Load Balancer"
    service_code = 'elasticloadbalancing'
    quota_code = 'L-57A373D6'
    instance_id = 'Load Balancer ARN'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [alb['LoadBalancerArn'] for alb in get_nlbs(session)]

    @property
    def current(self):
        try:
            return len(
                self.boto_session.client('elbv2').describe_listeners(
                    LoadBalancerArn=self.instance_id
                )['Listeners']
            )
        except self.boto_session.client('elbv2').exceptions.LoadBalancerNotFoundException as e:
            raise InstanceWithIdentifierNotFound(self) from e


class ApplicationLoadBalancerCountCheck(QuotaCheck):
    key = "elb_alb_count"
    description = "Application Load Balancers per region"
    scope = QuotaScope.REGION
    service_code = 'elasticloadbalancing'
    quota_code = 'L-53DA6B97'

    @property
    def current(self):
        return len(get_albs(self.boto_session))


class ListenerPerApplicationLoadBalancerCountCheck(InstanceQuotaCheck):
    key = "elb_listeners_per_alb"
    description = "Listeners per Application Load Balancer"
    service_code = 'elasticloadbalancing'
    quota_code = 'L-B6DF7632'
    instance_id = 'Load Balancer ARN'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [alb['LoadBalancerArn'] for alb in get_albs(session)]

    @property
    def current(self) -> int:
        try:
            return len(
                self.boto_session.client('elbv2').describe_listeners(
                    LoadBalancerArn=self.instance_id
                )['Listeners']
            )
        except self.boto_session.client('elbv2').exceptions.LoadBalancerNotFoundException as e:
            raise InstanceWithIdentifierNotFound(self) from e


class TargetGroupCountCheck(QuotaCheck):
    key = "elb_target_group_count"
    description = "Target Groups per region"
    scope = QuotaScope.REGION
    service_code = 'elasticloadbalancing'
    quota_code = 'L-B22855CB'

    @property
    def current(self):
        return len(self.boto_session.client('elbv2').describe_target_groups()['TargetGroups'])


class TargetGroupsPerApplicationLoadBalancerCountCheck(InstanceQuotaCheck):
    key = "elb_target_groups_per_alb"
    description = "Target groups per Application Load Balancer"
    service_code = 'elasticloadbalancing'
    quota_code = 'L-822D1B1B'
    instance_id = 'Load Balancer ARN'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [alb['LoadBalancerArn'] for alb in get_albs(session)]

    @property
    def current(self) -> int:
        try:
            return len(
                self.boto_session.client('elbv2').describe_target_groups(
                    LoadBalancerArn=self.instance_id
                )['TargetGroups']
            )
        except self.boto_session.client('elbv2').exceptions.LoadBalancerNotFoundException as e:
            raise InstanceWithIdentifierNotFound(self) from e
