from aws_quota.exceptions import InstanceWithIdentifierNotFound
import typing
import boto3
from .quota_check import InstanceQuotaCheck, QuotaCheck, QuotaScope


class HostedZoneCountCheck(QuotaCheck):
    key = "route53_hosted_zone_count"
    description = "Route53 Hosted Zones per Account"
    scope = QuotaScope.ACCOUNT

    @property
    def maximum(self):
        return self.boto_session.client('route53').get_account_limit(Type='MAX_HOSTED_ZONES_BY_OWNER')['Limit']['Value']

    @property
    def current(self):
        return self.boto_session.client('route53').get_account_limit(Type='MAX_HOSTED_ZONES_BY_OWNER')['Count']


class HealthCheckCountCheck(QuotaCheck):
    key = "route53_health_check_count"
    description = "Route53 Health Checks per Account"
    scope = QuotaScope.ACCOUNT

    @property
    def maximum(self):
        return self.boto_session.client('route53').get_account_limit(Type='MAX_HEALTH_CHECKS_BY_OWNER')['Limit']['Value']

    @property
    def current(self):
        return self.boto_session.client('route53').get_account_limit(Type='MAX_HEALTH_CHECKS_BY_OWNER')['Count']


class ReusableDelegationSetCountCheck(QuotaCheck):
    key = "route53_reusable_delegation_set_count"
    description = "Route53 Reusable Delegation Sets per Account"
    scope = QuotaScope.ACCOUNT

    @property
    def maximum(self):
        return self.boto_session.client('route53').get_account_limit(Type='MAX_REUSABLE_DELEGATION_SETS_BY_OWNER')['Limit']['Value']

    @property
    def current(self):
        return self.boto_session.client('route53').get_account_limit(Type='MAX_REUSABLE_DELEGATION_SETS_BY_OWNER')['Count']


class TrafficPolicyCountCheck(QuotaCheck):
    key = "route53_traffic_policy_count"
    description = "Route53 Traffic Policies per Account"
    scope = QuotaScope.ACCOUNT

    @property
    def maximum(self):
        return self.boto_session.client('route53').get_account_limit(Type='MAX_TRAFFIC_POLICIES_BY_OWNER')['Limit']['Value']

    @property
    def current(self):
        return self.boto_session.client('route53').get_account_limit(Type='MAX_TRAFFIC_POLICIES_BY_OWNER')['Count']


class TrafficPolicyInstanceCountCheck(QuotaCheck):
    key = "route53_traffic_policy_instance_count"
    description = "Route53 Traffic Policy Instances per Account"
    scope = QuotaScope.ACCOUNT

    @property
    def maximum(self):
        return self.boto_session.client('route53').get_account_limit(Type='MAX_TRAFFIC_POLICY_INSTANCES_BY_OWNER')['Limit']['Value']

    @property
    def current(self):
        return self.boto_session.client('route53').get_account_limit(Type='MAX_TRAFFIC_POLICY_INSTANCES_BY_OWNER')['Count']


class RecordsPerHostedZoneCheck(InstanceQuotaCheck):
    key = "route53_records_per_hosted_zone"
    description = "Records per Route53 Hosted Zone"
    instance_id = 'Hosted Zone ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [zone['Id'] for zone in session.client('route53').list_hosted_zones()['HostedZones']]

    @property
    def maximum(self):
        try:
            return self.boto_session.client('route53').get_hosted_zone_limit(Type='MAX_RRSETS_BY_ZONE', HostedZoneId=self.instance_id)['Limit']['Value']
        except self.boto_session.client('route53').exceptions.NoSuchHostedZone as e:
            raise InstanceWithIdentifierNotFound(self) from e

    @property
    def current(self):
        try:
            return self.boto_session.client('route53').get_hosted_zone_limit(Type='MAX_RRSETS_BY_ZONE', HostedZoneId=self.instance_id)['Count']
        except self.boto_session.client('route53').exceptions.NoSuchHostedZone as e:
            raise InstanceWithIdentifierNotFound(self) from e


class AssociatedVpcHostedZoneCheck(InstanceQuotaCheck):
    key = "route53_vpcs_per_hosted_zone"
    description = "Associated VPCs per Route53 Hosted Zone"
    instance_id = 'Hosted Zone ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [zone['Id'] for zone in session.client('route53').list_hosted_zones()['HostedZones'] if zone['Config']['PrivateZone']]

    @property
    def maximum(self):
        try:
            return self.boto_session.client('route53').get_hosted_zone_limit(Type='MAX_VPCS_ASSOCIATED_BY_ZONE', HostedZoneId=self.instance_id)['Limit']['Value']
        except self.boto_session.client('route53').exceptions.NoSuchHostedZone as e:
            raise InstanceWithIdentifierNotFound(self) from e

    @property
    def current(self):
        try:
            return self.boto_session.client('route53').get_hosted_zone_limit(Type='MAX_VPCS_ASSOCIATED_BY_ZONE', HostedZoneId=self.instance_id)['Count']
        except self.boto_session.client('route53').exceptions.NoSuchHostedZone as e:
            raise InstanceWithIdentifierNotFound(self) from e
