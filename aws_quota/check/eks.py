from .quota_check import QuotaCheck, QuotaScope


class ClusterCountCheck(QuotaCheck):
    key = "eks_count"
    description = "EKS Clusters per region"
    scope = QuotaScope.REGION
    service_code = 'eks'
    quota_code = 'L-1194D53C'

    @property
    def current(self):
        return len(self.boto_session.client('eks').list_clusters()['clusters'])
