from .quota_check import QuotaScope, RegionQuotaCheck


class RDSDBInstanceCountCheck(RegionQuotaCheck):
    key = "rds_instances"
    description = "RDS instances per Region"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-7B6409FD"

    @property
    def current(self) -> int:
        return self.count_paginated_results(
            "rds", "describe_db_instances", "DBInstances"
        )


class RDSDBParameterGroupsCountCheck(RegionQuotaCheck):
    key = "rds_parameter_groups"
    description = "RDS parameter groups per Region"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-DE55804A"

    @property
    def current(self) -> int:
        return self.count_paginated_results(
            "rds", "describe_db_parameter_groups", "DBParameterGroups"
        )


class RDSDBClusterParameterGroupCountCheck(RegionQuotaCheck):
    key = "rds_cluster_parameter_groups"
    description = "RDS cluster parameter groups per Region"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-E4C808A8"

    @property
    def current(self) -> int:
        return self.count_paginated_results(
            "rds", "describe_db_cluster_parameter_groups", "DBClusterParameterGroups"
        )


class RDSEventSubscriptions(RegionQuotaCheck):
    key = "rds_event_subscriptions"
    description = "RDS event subscriptions per Region"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-A59F4C87"

    @property
    def current(self) -> int:
        return self.count_paginated_results(
            "rds", "describe_event_subscriptions", "EventSubscriptionsList"
        )


class RDSDBSnapshotsCheck(RegionQuotaCheck):
    key = "rds_instance_snapshots"
    description = "Manual DB instance snapshots per Region"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-272F1212"

    @property
    def current(self) -> int:
        return self.count_paginated_results(
            "rds", "describe_db_snapshots", "DBSnapshots", {"SnapshotType": "manual"}
        )


class RDSDBClusterSnapshotsCheck(RegionQuotaCheck):
    key = "rds_cluster_snapshots"
    description = "Manual DB cluster snapshots per Region"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-9B510759"

    @property
    def current(self) -> int:
        return self.count_paginated_results(
            "rds", "describe_db_cluster_snapshots", "DBClusterSnapshots", {"SnapshotType": "manual"}
        )
