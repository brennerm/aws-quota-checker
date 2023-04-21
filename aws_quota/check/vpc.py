from aws_quota.exceptions import InstanceWithIdentifierNotFound
import typing

import boto3
import botocore.exceptions
import cachetools
from .quota_check import QuotaCheck, InstanceQuotaCheck, QuotaScope


def check_if_vpc_exists(session: boto3.Session, vpc_id: str) -> bool:
    client = session.client('ec2')
    try:
        client.describe_vpcs(VpcIds=[vpc_id])
    except botocore.exceptions.ClientError as e:
        return False
    return True


@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_vpcs(session: boto3.Session) -> typing.List[dict]:
    return session.client('ec2').describe_vpcs()['Vpcs']


def get_vpc_by_id(session: boto3.Session, vpc_id: str) -> dict:
    try:
        return next(filter(lambda vpc: vpc_id == vpc['VpcId'], get_all_vpcs(session)))
    except StopIteration:
        raise KeyError


@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_vpc_peering_connections(session: boto3.Session) -> typing.List[dict]:
    return session.client('ec2').describe_vpc_peering_connections(
            Filters=[
                {'Name': 'status-code', 'Values': ['active']},
            ]
         )['VpcPeeringConnections']

@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_sgs(session: boto3.Session) -> typing.List[dict]:
    return session.client('ec2').describe_security_groups()['SecurityGroups']


def get_sg_by_id(session: boto3.Session, sg_id: str) -> dict:
    try:
        return next(filter(lambda sg: sg_id == sg['GroupId'], get_all_sgs(session)))
    except StopIteration:
        raise KeyError


@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_rts(session: boto3.Session) -> typing.List[dict]:
    return session.client('ec2').describe_route_tables()['RouteTables']


def get_rt_by_id(session: boto3.Session, rt_id: str) -> dict:
    try:
        return next(filter(lambda rt: rt_id == rt['RouteTableId'], get_all_rts(session)))
    except StopIteration:
        raise KeyError


@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_network_acls(session: boto3.Session) -> typing.List[dict]:
    return session.client('ec2').describe_network_acls()['NetworkAcls']


class VpcCountCheck(QuotaCheck):
    key = "vpc_count"
    description = "VPCs per Region"
    scope = QuotaScope.REGION
    service_code = 'vpc'
    quota_code = 'L-F678F1CE'

    @property
    def current(self):
        return len(get_all_vpcs(self.boto_session))


class InternetGatewayCountCheck(QuotaCheck):
    key = "ig_count"
    description = "VPC internet gateways per Region"
    scope = QuotaScope.REGION
    service_code = 'vpc'
    quota_code = 'L-A4707A72'

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_internet_gateways()['InternetGateways'])


class NetworkInterfaceCountCheck(QuotaCheck):
    key = "ni_count"
    description = "VPC network interfaces per Region"
    scope = QuotaScope.REGION
    service_code = 'vpc'
    quota_code = 'L-DF5E4CA3'

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_network_interfaces()['NetworkInterfaces'])


class SecurityGroupCountCheck(QuotaCheck):
    key = "sg_count"
    description = "VPC security groups per Region"
    scope = QuotaScope.REGION
    service_code = 'vpc'
    quota_code = 'L-E79EC296'

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_security_groups()['SecurityGroups'])


class RulesPerSecurityGroupCheck(InstanceQuotaCheck):
    key = "vpc_rules_per_sg"
    description = "Rules per VPC security group"
    service_code = 'vpc'
    quota_code = 'L-0EA8095F'
    instance_id = 'Security Group ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [sg['GroupId'] for sg in get_all_sgs(session)]

    @property
    def current(self):
        try:
            sg = get_sg_by_id(self.boto_session, self.instance_id)
            return len(sg['IpPermissions']) + len(sg['IpPermissionsEgress'])
        except KeyError:
            raise InstanceWithIdentifierNotFound(self)


class RouteTablesPerVpcCheck(InstanceQuotaCheck):
    key = "vpc_route_tables_per_vpc"
    description = "Route Tables per VPC"
    service_code = 'vpc'
    quota_code = 'L-589F43AA'
    instance_id = 'VPC ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [vpc['VpcId'] for vpc in get_all_vpcs(session)]

    @property
    def current(self):
        if check_if_vpc_exists(self.boto_session, self.instance_id):
            return len(self.boto_session.client('ec2').describe_route_tables(Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [self.instance_id]
                }])['RouteTables'])
        else:
            raise InstanceWithIdentifierNotFound(self)


class RoutesPerRouteTableCheck(InstanceQuotaCheck):
    key = "vpc_routes_per_route_table"
    description = "Routes per Route Table"
    service_code = 'vpc'
    quota_code = 'L-93826ACB'
    instance_id = 'Route Table ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [rt['RouteTableId'] for rt in get_all_rts(session)]

    @property
    def current(self):
        try:
            rt = get_rt_by_id(self.boto_session, self.instance_id)
            return len(rt['Routes'])
        except KeyError:
            raise InstanceWithIdentifierNotFound(self)


class SubnetsPerVpcCheck(InstanceQuotaCheck):
    key = "vpc_subnets_per_vpc"
    description = "Subnets per VPC"
    service_code = 'vpc'
    quota_code = 'L-407747CB'
    instance_id = 'VPC ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [vpc['VpcId'] for vpc in get_all_vpcs(session)]

    @property
    def current(self):
        if check_if_vpc_exists(self.boto_session, self.instance_id):
            return len(self.boto_session.client('ec2').describe_subnets(Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [self.instance_id]
                }])['Subnets'])
        else:
            raise InstanceWithIdentifierNotFound(self)


class AclsPerVpcCheck(InstanceQuotaCheck):
    key = "vpc_acls_per_vpc"
    description = "Network ACLs per VPC"
    service_code = 'vpc'
    quota_code = 'L-B4A6D682'
    instance_id = 'VPC ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [vpc['VpcId'] for vpc in get_all_vpcs(session)]

    @property
    def current(self) -> int:
        if check_if_vpc_exists(self.boto_session, self.instance_id):
            return len(self.boto_session.client('ec2').describe_network_acls(Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [self.instance_id]
                }])['NetworkAcls'])
        else:
            raise InstanceWithIdentifierNotFound(self)


class RulesPerAclCheck(InstanceQuotaCheck):
    key = "vpc_rules_per_acl"
    description = "Rules per Network ACL"
    service_code = 'vpc'
    quota_code = 'L-2AEEBF1A'
    instance_id = 'Network ACL ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [acl['NetworkAclId'] for acl in get_all_network_acls(session)]

    @property
    def current(self) -> int:
        acls = get_all_network_acls(self.boto_session)
        if self.instance_id in [acl['NetworkAclId'] for acl in acls]:
            return len(next(filter(lambda acl: self.instance_id == acl['NetworkAclId'], acls))['Entries'])
        else:
            raise InstanceWithIdentifierNotFound(self)


class Ipv4CidrBlocksPerVpcCheck(InstanceQuotaCheck):
    key = "vpc_ipv4_cidr_blocks_per_vpc"
    description = "IPv4 CIDR blocks per VPC"
    service_code = 'vpc'
    quota_code = 'L-83CA0A9D'
    instance_id = 'VPC ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [vpc['VpcId'] for vpc in get_all_vpcs(session)]

    @property
    def current(self) -> int:
        try:
            vpc = get_vpc_by_id(self.boto_session, self.instance_id)
            return len(list(filter(lambda cbas: cbas['CidrBlockState']['State'] == 'associated', vpc['CidrBlockAssociationSet'])))
        except KeyError:
            raise InstanceWithIdentifierNotFound(self)


class Ipv6CidrBlocksPerVpcCheck(InstanceQuotaCheck):
    key = "vpc_ipv6_cidr_blocks_per_vpc"
    description = "IPv6 CIDR blocks per VPC"
    service_code = 'vpc'
    quota_code = 'L-085A6257'
    instance_id = 'VPC ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [vpc['VpcId'] for vpc in get_all_vpcs(session)]

    @property
    def current(self) -> int:
        try:
            vpc = get_vpc_by_id(self.boto_session, self.instance_id)
            if 'Ipv6CidrBlockAssociationSet' not in vpc:
                return 0

            return len(list(filter(lambda cbas: cbas['Ipv6CidrBlockState']['State'] == 'associated', vpc['Ipv6CidrBlockAssociationSet'])))
        except KeyError:
            raise InstanceWithIdentifierNotFound(self)

class ActiveVpcPeeringConnectionsPerVpcCheck(InstanceQuotaCheck):
    key = "vpc_peering_connections_per_vpc"
    description = "Active VPC peering connections per VPC"
    service_code = 'vpc'
    quota_code = 'L-7E9ECCDB'
    instance_id = 'VPC ID'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [vpc['VpcId'] for vpc in get_all_vpcs(session)]

    @property
    def current(self) -> int:
        peering_connections_per_vpc = 0
        try:
            vpc = get_vpc_by_id(self.boto_session, self.instance_id)
            vpc_peering_connections = get_vpc_peering_connections(self.boto_session)
            for peering_connection in vpc_peering_connections:
                for vpc_info in [peering_connection['AccepterVpcInfo'], peering_connection['RequesterVpcInfo']]:
                    if vpc_info['VpcId'] == vpc['VpcId'] and self.boto_session.region_name == vpc_info['Region']:
                        peering_connections_per_vpc += 1

            return peering_connections_per_vpc
        except KeyError:
            raise InstanceWithIdentifierNotFound(self)
