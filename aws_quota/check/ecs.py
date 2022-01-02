from .quota_check import QuotaCheck, QuotaScope

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
            ],
            MaxResults=1000
            )['Reservations'] for instance in reservations['Instances']]

class ClusterCountCheck(QuotaCheck):
    key = "ecs_count"
    description = "ECS Clusters per region"
    scope = QuotaScope.REGION
    service_code = 'ecs'
    quota_code = 'L-21C621EB'

    @property
    def current(self):
        return len(self.boto_session.client('ecs').list_clusters()['clusterArns'])

class FargateSpotCountCheck(QuotaCheck):
    key = "fargatespot_count"
    description = "Fargate Spot in this account in the current Region"
    scope = QuotaScope.REGION
    service_code = 'fargate'
    quota_code = 'L-1F0160F4'

    @property
    def current(self):
        return len(self.boto_session.client('ecs').list_clusters()['clusterArns'])

class FargateDemandCountCheck(QuotaCheck):
    key = "fargatedemand_count"
    description = "Fargate On-Demand resource count in the current Region"
    scope = QuotaScope.REGION
    service_code = 'fargate'
    quota_code = 'L-790AF391'

    @property
    def current(self):
        return len(self.boto_session.client('ecs').list_clusters()['clusterArns'])        