from .quota_check import RegionQuotaCheck, QuotaScope


class ClusterCountCheck(RegionQuotaCheck):
    key = "ecs_count"
    description = "ECS Clusters per Region"
    scope = QuotaScope.REGION
    service_code = 'ecs'
    quota_code = 'L-21C621EB'

    @property
    def current(self):
        return len(self.boto_session.client('ecs').list_clusters()['clusterArns'])
