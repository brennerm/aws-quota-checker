from .quota_check import QuotaCheck, QuotaScope


class TableCountCheck(QuotaCheck):
    key = "dyndb_table_count"
    description = "DynamoDB Tables per Region"
    scope = QuotaScope.REGION
    service_code = 'dynamodb'
    quota_code = 'L-F98FE922'

    @property
    def current(self):
        return self.count_paginated_results("dynamodb", "list_tables", "TableNames" )
