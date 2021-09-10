from .appmesh import *
from .autoscaling import *
from .cloudformation import *
from .cloudwatch import *
from .dynamodb import *
from .ebs import *
from .ec2 import *
from .ecs import *
from .eks import *
from .elasticbeanstalk import *
from .elb import *
from .iam import *
from .lambdas import *
from .route53 import *
from .route53resolver import *
from .s3 import *
from .sns import *
from .secretsmanager import *
from .vpc import *
from .rds import *
from .quota_check import QuotaCheck


def __all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in __all_subclasses(c)]
    )


ALL_CHECKS = sorted(
    [clazz for clazz in __all_subclasses(QuotaCheck) if clazz != InstanceQuotaCheck],
    key=lambda clz: clz.key,
)
ALL_INSTANCE_SCOPED_CHECKS = list(filter(lambda check: check.scope == QuotaScope.INSTANCE, ALL_CHECKS))
