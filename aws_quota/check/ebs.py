from .quota_check import QuotaCheck, QuotaScope


class SnapshotCountCheck(QuotaCheck):
    key = "ebs_snapshot_count"
    description = "EBS Snapshots per Region"
    scope = QuotaScope.REGION
    service_code = 'ebs'
    quota_code = 'L-309BACF6'

    @property
    def current(self):
        return self.count_paginated_results("ec2", "describe_snapshots", "Snapshots", {"OwnerIds": ["self"]})
