from .quota_check import QuotaCheck, QuotaScope


class OnDemandStandardInstanceCountCheck(QuotaCheck):
    key = "ec2_on_demand_standard_count"
    description = "Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) EC2 instances"
    scope = QuotaScope.ACCOUNT
    service_code = "ec2"
    quota_code = "L-1216C47A"

    @property
    def current(self):
        instances = [instance for reservations in self.boto_session.client('ec2').describe_instances(
            Filters=[
                {
                    'Name': 'instance-state-name',
                    'Values': ['running']
                }
            ]
        )['Reservations'] for instance in reservations['Instances']]

        return len(list(filter(lambda inst: inst['InstanceType'][0] in ['a', 'c', 'd', 'h', 'i', 'm', 'r', 't', 'z', ], instances)))


class SpotStandardRequestCountCheck(QuotaCheck):
    key = "ec2_spot_standard_count"
    description = "All Standard (A, C, D, H, I, M, R, T, Z) EC2 Spot Instance Requests"
    scope = QuotaScope.ACCOUNT
    service_code = "ec2"
    quota_code = "L-34B43A08"

    @property
    def current(self):
        requests = self.boto_session.client('ec2').describe_spot_instance_requests()[
            'SpotInstanceRequests']

        return len(list(filter(lambda inst: inst['LaunchSpecification']['InstanceType'][0] in ['a', 'c', 'd', 'h', 'i', 'm', 'r', 't', 'z', ], requests)))


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
    description = "Transit Gateways per account"
    scope = QuotaScope.ACCOUNT
    service_code = 'ec2'
    quota_code = 'L-A2478D36'

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_transit_gateways()['TransitGateways'])

class VpnConnectionCountCheck(QuotaCheck):
    key = "ec2_vpn_connection_count"
    description = "VPN connections per region"
    scope = QuotaScope.REGION
    service_code = 'ec2'
    quota_code = 'L-3E6EC3A3'

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_vpn_connections()['VpnConnections'])
