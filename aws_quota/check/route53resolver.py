from .quota_check import QuotaCheck, QuotaScope


class EndpointCountCheck(QuotaCheck):
    key = "route53resolver_endpoint_count"
    description = "Route53 Resolver endpoints per region"
    scope = QuotaScope.REGION
    service_code = 'route53resolver'
    quota_code = 'L-4A669CC0'

    @property
    def current(self):
        return len(self.boto_session.client('route53resolver').list_resolver_endpoints()['ResolverEndpoints'])

class RulesCountCheck(QuotaCheck):
    key = "route53resolver_rule_count"
    description = "Route53 Resolver rules per region"
    scope = QuotaScope.REGION
    service_code = 'route53resolver'
    quota_code = 'L-51D8A1FB'

    @property
    def current(self):
        return len(self.boto_session.client('route53resolver').list_resolver_rules()['ResolverRules'])

class RuleAssociationsCountCheck(QuotaCheck):
    key = "route53resolver_rule_association_count"
    description = "Route53 Resolver rule associations per region"
    scope = QuotaScope.REGION
    service_code = 'route53resolver'
    quota_code = 'L-94E19253'

    @property
    def current(self):
        return len(self.boto_session.client('route53resolver').list_resolver_rule_associations()['ResolverRuleAssociations'])
