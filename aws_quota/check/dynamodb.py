from .quota_check import QuotaCheck, QuotaScope


class TableCountCheck(QuotaCheck):
    key = "dyndb_table_count"
    description = "DynamoDB Tables per region"
    scope = QuotaScope.REGION
    service_code = 'dynamodb'
    quota_code = 'L-F98FE922'

    @property
    def current(self):
        return len(self.boto_session.client('dynamodb').list_tables()['TableNames'])
