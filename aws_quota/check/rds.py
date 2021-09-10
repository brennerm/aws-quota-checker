from .quota_check import QuotaCheck, QuotaScope

class RDSDBInstanceCountCheck(QuotaCheck):
    key = "rds_instances"
    description = "RDS instances per region"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-7B6409FD"

    @property
    def current(self) -> int:
        return self.count_paginated_results("rds", "describe_db_instances", "DBInstances")

class RDSDBParameterGroupsCountCheck(QuotaCheck):
    key = "rds_parameter_groups"
    description = "RDS parameter groups per region"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-DE55804A"

    @property
    def current(self) -> int:
        return self.count_paginated_results("rds", "describe_db_parameter_groups", "DBParameterGroups")


class RDSDBClusterParameterGroupCountCheck(QuotaCheck):
    key = "rds_cluster_parameter_groups"
    description = "RDS cluster parameter groups per region"
    service_code = "rds"
    scope = QuotaScope.REGION
    quota_code = "L-E4C808A8"

    @property
    def current(self) -> int:
        return self.count_paginated_results("rds", "describe_db_cluster_parameter_groups", "DBClusterParameterGroups")
