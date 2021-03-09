from aws_quota.exceptions import InstanceWithIdentifierNotFound
import typing

import boto3
from .quota_check import QuotaCheck, InstanceQuotaCheck, QuotaScope


class TopicCountCheck(QuotaCheck):
    key = "sns_topics_count"
    description = "SNS topics per account"
    scope = QuotaScope.ACCOUNT
    service_code = 'sns'
    quota_code = 'L-61103206'

    @property
    def current(self):
        return len(self.boto_session.client('sns').list_topics()['Topics'])

class PendingSubscriptionCountCheck(QuotaCheck):
    key = "sns_pending_subscriptions_count"
    description = "Pending SNS subscriptions per account"
    scope = QuotaScope.ACCOUNT
    service_code = 'sns'
    quota_code = 'L-1A43D3DB'

    @property
    def current(self):
        all_topic_arns = SubscriptionsPerTopicCheck.get_all_identifiers(self.boto_session)
        pending_subs = 0

        for arn in all_topic_arns:
            pending_subs += int(self.boto_session.client('sns').get_topic_attributes(TopicArn=arn)['Attributes']['SubscriptionsPending'])

        return pending_subs

class SubscriptionsPerTopicCheck(InstanceQuotaCheck):
    key = "sns_subscriptions_per_topic"
    description = "SNS subscriptions per topics"
    service_code = 'sns'
    quota_code = 'L-A4340BCD'
    instance_id = 'Topic ARN'

    @staticmethod
    def get_all_identifiers(session: boto3.Session) -> typing.List[str]:
        return [topic['TopicArn'] for topic in session.client('sns').list_topics()['Topics']]

    @property
    def current(self):
        try:
            topic_attrs = self.boto_session.client('sns').get_topic_attributes(TopicArn=self.instance_id)['Attributes']
        except self.boto_session.client('sns').exceptions.NotFoundException as e:
            raise InstanceWithIdentifierNotFound(self) from e

        return int(topic_attrs['SubscriptionsConfirmed']) + int(topic_attrs['SubscriptionsPending'])
