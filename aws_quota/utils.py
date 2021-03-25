import functools
import boto3


@functools.lru_cache()
def get_account_id(session: boto3.Session) -> str:
    return session.client('sts').get_caller_identity()['Account']