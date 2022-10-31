from .quota_check import QuotaScope, RegionQuotaCheck


class TableCountCheck(RegionQuotaCheck):
    key = "dyndb_table_count"
    description = "DynamoDB Tables per Region"
    scope = QuotaScope.REGION
    service_code = 'dynamodb'
    quota_code = 'L-F98FE922'

    @property
    def current(self):
        return len(self.boto_session.client('dynamodb').list_tables()['TableNames'])
