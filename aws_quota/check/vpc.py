import typing

import boto3
from .quota_check import QuotaCheck, InstanceQuotaCheck, QuotaScope


class VpcCountCheck(QuotaCheck):
    key = "vpc_count"
    description = "VPCs per region"
    scope = QuotaScope.REGION
    service_code = 'vpc'
    quota_code = 'L-F678F1CE'

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_vpcs()['Vpcs'])


class InternetGatewayCountCheck(QuotaCheck):
    key = "ig_count"
    description = "VPC internet gateways per region"
    scope = QuotaScope.REGION
    service_code = 'vpc'
    quota_code = 'L-A4707A72'

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_internet_gateways()['InternetGateways'])


class NetworkInterfaceCountCheck(QuotaCheck):
    key = "ni_count"
    description = "VPC network interfaces per region"
    scope = QuotaScope.REGION
    service_code = 'vpc'
    quota_code = 'L-DF5E4CA3'

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_network_interfaces()['NetworkInterfaces'])


class SecurityGroupCountCheck(QuotaCheck):
    key = "sg_count"
    description = "VPC security groups per region"
    scope = QuotaScope.REGION
    service_code = 'vpc'
    quota_code = 'L-E79EC296'

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_security_groups()['SecurityGroups'])


class SubnetsPerVpcCountCheck(InstanceQuotaCheck):
    key = "vpc_subnets_per_vpc"
    description = "Subnets per VPC"
    service_code = 'vpc'
    quota_code = 'L-407747CB'
    instance_id = 'VPC ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [vpc['VpcId'] for vpc in session.client(
                'ec2').describe_vpcs()['Vpcs']]

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_subnets(Filters=[
            {
                'Name': 'vpc-id',
                'Values': [self.instance_id]
            }])['Subnets'])


class AclsPerVpcCountCheck(InstanceQuotaCheck):
    key = "vpc_acls_per_vpc"
    description = "Network ACLs per VPC"
    service_code = 'vpc'
    quota_code = 'L-B4A6D682'
    instance_id = 'VPC ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [vpc['VpcId'] for vpc in session.client('ec2').describe_vpcs()['Vpcs']]

    @property
    def current(self) -> int:
        return len(self.boto_session.client('ec2').describe_network_acls(Filters=[
            {
                'Name': 'vpc-id',
                'Values': [self.instance_id]
            }])['NetworkAcls'])
