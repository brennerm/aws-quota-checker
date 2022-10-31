from .quota_check import RegionQuotaCheck, QuotaScope


class BucketCountCheck(RegionQuotaCheck):
    key = "s3_bucket_count"
    description = "S3 Buckets per Account"
    scope = QuotaScope.REGION
    service_code = 's3'
    quota_code = 'L-DC2B2D3D'

    @property
    def current(self):
        return len(self.boto_session.client('s3').list_buckets()['Buckets'])
