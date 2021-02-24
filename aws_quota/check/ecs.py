from .quota_check import QuotaCheck, QuotaScope


class ClusterCountCheck(QuotaCheck):
    key = "ecs_count"
    description = "ECS Clusters per region"
    scope = QuotaScope.REGION
    service_code = 'ecs'
    quota_code = 'L-21C621EB'

    @property
    def current(self):
        return len(self.boto_session.client('ecs').list_clusters()['clusterArns'])
