from .quota_check import QuotaCheck, QuotaScope


class SnapshotCountCheck(QuotaCheck):
    key = "ebs_snapshot_count"
    description = "EBS Snapshots per region"
    scope = QuotaScope.REGION
    service_code = 'ebs'
    quota_code = 'L-309BACF6'

    @property
    def current(self):
        return len(self.boto_session.client('ec2').describe_snapshots(OwnerIds=['self'])['Snapshots'])
