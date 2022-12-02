from .quota_check import QuotaCheck, QuotaScope, RegionQuotaCheck

import boto3
import cachetools


@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_running_ec2_instances(session: boto3.Session):
    return [instance for reservations in session.client('ec2').describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }
            ]
            )['Reservations'] for instance in reservations['Instances']]


@cachetools.cached(cache=cachetools.TTLCache(1, 60))
def get_all_spot_requests(session: boto3.Session):
    return session.client('ec2').describe_spot_instance_requests()[
        'SpotInstanceRequests']


class OnDemandStandardInstanceCountCheck(RegionQuotaCheck):
    key = "ec2_on_demand_standard_count"
    description = "Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) EC2 instances"
    scope = QuotaScope.ACCOUNT
    service_code = "ec2"
    quota_code = "L-1216C47A"

    @property
    def current(self):
        instances = get_all_running_ec2_instances(self.boto_session)

        return len(list(filter(lambda inst: inst['InstanceType'][0] in ['a', 'c', 'd', 'h', 'i', 'm', 'r', 't', 'z'], instances)))


class OnDemandFInstanceCountCheck(QuotaCheck):
    key = "ec2_on_demand_f_count"
    description = "Running On-Demand F EC2 instances"
    scope = QuotaScope.ACCOUNT
    service_code = "ec2"
    quota_code = "L-74FC7D96"

    @property
    def current(self):
        instances = get_all_running_ec2_instances(self.boto_session)

        return len(list(filter(lambda inst: inst['InstanceType'][0] in ['f'], instances)))


class OnDemandGInstanceCountCheck(QuotaCheck):
    key = "ec2_on_demand_g_count"
    description = "Running On-Demand G EC2 instances"
    scope = QuotaScope.ACCOUNT
    service_code = "ec2"
    quota_code = "L-DB2E81BA"

    @property
    def current(self):
        instances = get_all_running_ec2_instances(self.boto_session)

        return len(list(filter(lambda inst: inst['InstanceType'][0] in ['g'], instances)))


class OnDemandInfInstanceCountCheck(QuotaCheck):
    key = "ec2_on_demand_inf_count"
    description = "Running On-Demand Inf EC2 instances"
    scope = QuotaScope.ACCOUNT
    service_code = "ec2"
    quota_code = "L-1945791B"

    @property
    def current(self):
        instances = get_all_running_ec2_instances(self.boto_session)

        return len(list(filter(lambda inst: inst['InstanceType'][0] in ['inf'], instances)))


class OnDemandPInstanceCountCheck(QuotaCheck):
    key = "ec2_on_demand_p_count"
    description = "Running On-Demand P EC2 instances"
    scope = QuotaScope.ACCOUNT
    service_code = "ec2"
    quota_code = "L-417A185B"

    @property
    def current(self):
        instances = get_all_running_ec2_instances(self.boto_session)

        return len(list(filter(lambda inst: inst['InstanceType'][0] in ['p'], instances)))


class OnDemandXInstanceCountCheck(QuotaCheck):
    key = "ec2_on_demand_x_count"
    description = "Running On-Demand X EC2 instances"
    scope = QuotaScope.ACCOUNT
    service_code = "ec2"
    quota_code = "L-7295265B"

    @property
    def current(self):
        instances = get_all_running_ec2_instances(self.boto_session)

        return len(list(filter(lambda inst: inst['InstanceType'][0] in ['x'], instances)))


class SpotStandardRequestCountCheck(QuotaCheck):
    key = "ec2_spot_standard_count"
    description = "All Standard (A, C, D, H, I, M, R, T, Z) EC2 Spot Instance Requests"
    scope = QuotaScope.ACCOUNT
    service_code = "ec2"
    quota_code = "L-34B43A08"

    @property
    def current(self):
        requests = get_all_spot_requests(self.boto_session)

        return len(list(filter(lambda inst: inst['LaunchSpecification']['InstanceType'][0] in ['a', 'c', 'd', 'h', 'i', 'm', 'r', 't', 'z'], requests)))


class SpotFRequestCountCheck(QuotaCheck):
    key = "ec2_spot_f_count"
    description = "All F EC2 Spot Instance Requests"
    scope = QuotaScope.ACCOUNT
    service_code = "ec2"
    quota_code = "L-88CF9481"

    @property
    def current(self):
        requests = get_all_spot_requests(self.boto_session)

        return len(list(filter(lambda inst: inst['LaunchSpecification']['InstanceType'][0] in ['f'], requests)))


class SpotGRequestCountCheck(QuotaCheck):
    key = "ec2_spot_g_count"
    description = "All G EC2 Spot Instance Requests"
    scope = QuotaScope.ACCOUNT
    service_code = "ec2"
    quota_code = "L-3819A6DF"

    @property
    def current(self):
        requests = get_all_spot_requests(self.boto_session)

        return len(list(filter(lambda inst: inst['LaunchSpecification']['InstanceType'][0] in ['g'], requests)))


class SpotInfRequestCountCheck(QuotaCheck):
    key = "ec2_spot_inf_count"
    description = "All Inf EC2 Spot Instance Requests"
    scope = QuotaScope.ACCOUNT
    service_code = "ec2"
    quota_code = "L-B5D1601B"

    @property
    def current(self):
        requests = get_all_spot_requests(self.boto_session)

        return len(list(filter(lambda inst: inst['LaunchSpecification']['InstanceType'][0] in ['inf'], requests)))


class SpotPRequestCountCheck(QuotaCheck):
    key = "ec2_spot_p_count"
    description = "All P EC2 Spot Instance Requests"
    scope = QuotaScope.ACCOUNT
    service_code = "ec2"
    quota_code = "L-7212CCBC"

    @property
    def current(self):
        requests = get_all_spot_requests(self.boto_session)

        return len(list(filter(lambda inst: inst['LaunchSpecification']['InstanceType'][0] in ['p'], requests)))


class SpotXRequestCountCheck(QuotaCheck):
    key = "ec2_spot_x_count"
    description = "All X EC2 Spot Instance Requests"
    scope = QuotaScope.ACCOUNT
    service_code = "ec2"
    quota_code = "L-E3A00192"

    @property
    def current(self):
        requests = get_all_spot_requests(self.boto_session)

        return len(list(filter(lambda inst: inst['LaunchSpecification']['InstanceType'][0] in ['x'], requests)))


class ElasticIpCountCheck(QuotaCheck):
    key = "ec2_eip_count"
    description = "EC2 VPC Elastic IPs"
    scope = QuotaScope.ACCOUNT
    service_code = 'ec2'
    quota_code = 'L-0263D0A3'

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_addresses()['Addresses'])


class TransitGatewayCountCheck(QuotaCheck):
    key = "ec2_tgw_count"
    description = "Transit Gateways per Account"
    scope = QuotaScope.ACCOUNT
    service_code = 'ec2'
    quota_code = 'L-A2478D36'

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_transit_gateways()['TransitGateways'])


class VpnConnectionCountCheck(RegionQuotaCheck):
    key = "ec2_vpn_connection_count"
    description = "VPN connections per Region"
    scope = QuotaScope.REGION
    service_code = 'ec2'
    quota_code = 'L-3E6EC3A3'

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_vpn_connections()['VpnConnections'])
