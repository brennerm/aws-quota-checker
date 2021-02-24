import enum
import typing

import boto3


class QuotaScope(enum.Enum):
    ACCOUNT = 0
    REGION = 1
    INSTANCE = 2


class QuotaCheck:
    key: str = None
    description: str = None
    scope: QuotaScope = None
    service_code: str = None
    quota_code: str = None

    def __init__(self, boto_session: boto3.Session) -> None:
        super().__init__()

        self.boto_session = boto_session
        self.sq_client = boto_session.client('service-quotas')

    @property
    def maximum(self) -> int:
        try:
            return int(self.sq_client.get_service_quota(ServiceCode=self.service_code, QuotaCode=self.quota_code)['Quota']['Value'])
        except self.sq_client.exceptions.NoSuchResourceException:
            return int(self.sq_client.get_aws_default_service_quota(ServiceCode=self.service_code, QuotaCode=self.quota_code)['Quota']['Value'])

    @property
    def current(self) -> int:
        raise NotImplementedError


class InstanceQuotaCheck(QuotaCheck):
    scope = QuotaScope.INSTANCE
    instance_id: str = None

    def __init__(self, boto_session: boto3.Session, instance_id) -> None:
        super().__init__(boto_session)

        self.instance_id = instance_id

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        raise NotImplementedError
