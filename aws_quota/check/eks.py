from .quota_check import RegionQuotaCheck, QuotaScope


class ClusterCountCheck(RegionQuotaCheck):
    key = "eks_count"
    description = "EKS Clusters per Region"
    scope = QuotaScope.REGION
    service_code = 'eks'
    quota_code = 'L-1194D53C'

    @property
    def current(self):
        return len(self.boto_session.client('eks').list_clusters()['clusters'])
