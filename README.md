# aws-quota-checker

A tool that helps keeping track of your AWS quota utilization. It'll determine the limits of your AWS account and compare them to the number of current resources.

![Example output of aws-quota-checker](https://raw.githubusercontent.com/brennerm/aws-quota-checker/master/img/example.png)

This is especially useful cause today, cloud resources are being created from all kinds of sources, e.g. IaC and Kubernetes operators. This tool will give you a head start for requesting quota increases before you hit a quota limit to prevent being stuck with a production system not being able to scale anymore.

A usual use case is to add it to your CI pipeline right after applying your IaC or run it on a regular basis. It also comes with a Prometheus exporter mode that allows you to visualize the data with your tool of choice, e.g. Grafana.

![Example Grafana dashboard that uses metrics of the Prometheus exporter](https://raw.githubusercontent.com/brennerm/aws-quota-checker/master/img/example-grafana-dashboard.png)

## Installation

### From pypi

```bash
pip install aws-quota-checker
```

### From Docker

```bash
docker run -e AWS_ACCESS_KEY_ID=ABC -e AWS_SECRET_ACCESS_KEY=DEF -e AWS_DEFAULT_REGION=eu-central-1 ghcr.io/brennerm/aws-quota-checker
```

or

```bash
aws configure
docker run -v ~/.aws/credentials:/home/aqc/.aws/credentials:ro ghcr.io/brennerm/aws-quota-checker
```

### From source

```bash
git clone git@github.com:brennerm/aws-quota-checker.git
cd aws-quota-checker
pip install .
```

## Usage

Make sure you are logged into your AWS account (`aws configure` or through environment variables) or switch to the one you want to check. This account needs to have read permissions for all supported services. AWS provides a default policy called _ReadOnlyAccess_ that contains the required permissions.

Check the help page with `aws-quota-checker --help` to see all available command and their documentation.

### Run a single check

```bash
$ aws-quota-checker check vpc_count
AWS profile: default | AWS region: eu-central-1 | Active checks: vpc_count
VPCs per region [default/eu-central-1]: 1/5 ✓
```

### Run all checks

```bash
$ aws-quota-checker check all
AWS profile: default | AWS region: eu-central-1 | Active checks: route53_traffic_policy_count,vpc_count,ec2_tgw_count,ec2_on_demand_standard_count,route53_health_check_count,cw_alarm_count,iam_attached_policy_per_role,asg_count,elasticbeanstalk_environment_count,s3_bucket_count,iam_attached_policy_per_user,elb_listeners_per_alb,ec2_eip_count,route53resolver_rule_count,iam_policy_version_count,elb_listeners_per_nlb,vpc_subnets_per_vpc,route53_vpcs_per_hosted_zone,cf_stack_count,iam_user_count,elb_listeners_per_clb,ni_count,dyndb_table_count,elasticbeanstalk_application_count,route53_traffic_policy_instance_count,ig_count,elb_clb_count,ec2_vpn_connection_count,route53_reusable_delegation_set_count,ebs_snapshot_count,route53_hosted_zone_count,iam_attached_policy_per_group,eks_count,am_mesh_count,elb_target_group_count,route53resolver_rule_association_count,iam_server_certificate_count,elb_alb_count,vpc_acls_per_vpc,iam_group_count,ec2_spot_standard_count,route53resolver_endpoint_count,iam_policy_count,elb_nlb_count,sg_count,route53_records_per_hosted_zone,lc_count,ecs_count,secretsmanager_secrets_count
Collecting checks  [####################################]  100%
Route53 Traffic Policies per Account [default]: 0/50 ✓
VPCs per region [default/eu-central-1]: 1/5 ✓
Transit Gateways per account [default]: 4/5 !
Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) EC2 instances [default]: 0/1280 ✓
Route53 Health Checks per Account [default]: 0/200 ✓
Number of CloudWatch alarms per region [default/eu-central-1]: 0/5000 ✓
Auto Scaling groups per region [default/eu-central-1]: 0/200 ✓
Elastic Beanstalk Environments per account [default]: 0/200 ✓
Application Load Balancers per region [default/eu-central-1]: 46/50 X
...
```

### Run a single instance check

```bash
$ aws-quota-checker check-instance vpc_acls_per_vpc vpc-0123456789
Network ACLs per VPC [default/eu-central-1/vpc-0123456789]: 0/200
```

### Prometheus exporter

The Prometheus exporter requires additional dependencies that you need to install with `pip install aws-quota-checker[prometheus]`.

```bash
$ aws-quota-checker prometheus-exporter all
AWS profile: default | AWS region: us-east-1 | Active checks: am_mesh_count,asg_count,cf_stack_count,cw_alarm_count,dyndb_table_count,ebs_snapshot_count,ec2_eip_count,ec2_on_demand_f_count,ec2_on_demand_g_count,ec2_on_demand_inf_count,ec2_on_demand_p_count,ec2_on_demand_standard_count,ec2_on_demand_x_count,ec2_spot_f_count,ec2_spot_g_count,ec2_spot_inf_count,ec2_spot_p_count,ec2_spot_standard_count,ec2_spot_x_count,ec2_tgw_count,ec2_vpn_connection_count,ecs_count,eks_count,elasticbeanstalk_application_count,elasticbeanstalk_environment_count,elb_alb_count,elb_clb_count,elb_listeners_per_alb,elb_listeners_per_clb,elb_listeners_per_nlb,elb_nlb_count,elb_target_group_count,iam_attached_policy_per_group,iam_attached_policy_per_role,iam_attached_policy_per_user,iam_group_count,iam_policy_count,iam_policy_version_count,iam_server_certificate_count,iam_user_count,ig_count,lc_count,ni_count,route53_health_check_count,route53_hosted_zone_count,route53_records_per_hosted_zone,route53_reusable_delegation_set_count,route53_traffic_policy_count,route53_traffic_policy_instance_count,route53_vpcs_per_hosted_zone,route53resolver_endpoint_count,route53resolver_rule_association_count,route53resolver_rule_count,s3_bucket_count,secretsmanager_secrets_count,sg_count,sns_pending_subscriptions_count,sns_subscriptions_per_topic,sns_topics_count,vpc_acls_per_vpc,vpc_count,vpc_subnets_per_vpc
09-Mar-21 20:15:11 [INFO] botocore.credentials - Found credentials in shared credentials file: ~/.aws/credentials
09-Mar-21 20:15:11 [INFO] aws_quota.prometheus - starting /metrics endpoint on port 8080
09-Mar-21 20:15:11 [INFO] aws_quota.prometheus - collecting checks
09-Mar-21 20:15:19 [INFO] aws_quota.prometheus - collected 110 checks
09-Mar-21 20:15:19 [INFO] aws_quota.prometheus - refreshing limits
09-Mar-21 20:16:34 [INFO] aws_quota.prometheus - limits refreshed
09-Mar-21 20:16:34 [INFO] aws_quota.prometheus - refreshing current values
09-Mar-21 20:18:15 [INFO] aws_quota.prometheus - current values refreshed
```

The exporter will return the following metrics:

- awsquota_$checkkey: the current value of each quota check
- awsquota_$checkkey_limit: the limit value of each quota check
- awsquota_check_count: the number of quota checks that are being executed
- awsquota_check_limits_duration_seconds: the number of seconds that was necessary to query all quota limits
- awsquota_check_currents_duration_seconds: the number of seconds that was necessary to query all current quota values
- awsquota_info: info gauge that will expose the current AWS account and region as labels

Depending on the check type, labels for the AWS account, the AWS region and the instance ID will be attached to the metric.

Below you can find a few example metrics:

```
# HELP awsquota_info AWS quota checker info
# TYPE awsquota_info gauge
awsquota_info{account="123456789",region="us-east-1"} 1.0
# HELP awsquota_check_count Number of AWS Quota Checks
# TYPE awsquota_check_count gauge
awsquota_check_count 110.0
# HELP awsquota_collect_checks_duration_seconds Time to collect all quota checks
# TYPE awsquota_collect_checks_duration_seconds gauge
awsquota_collect_checks_duration_seconds{account="123456789",region="us-east-1"} 7.885610818862915
# HELP awsquota_asg_count_limit Auto Scaling groups per region Limit
# TYPE awsquota_asg_count_limit gauge
awsquota_asg_count_limit{account="123456789",region="us-east-1"} 200.0
# HELP awsquota_ec2_on_demand_standard_count Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) EC2 instances
# TYPE awsquota_ec2_on_demand_standard_count gauge
awsquota_ec2_on_demand_standard_count{account="123456789"} 22.0
# HELP awsquota_elb_listeners_per_clb Listeners per Classic Load Balancer
# TYPE awsquota_elb_listeners_per_clb gauge
awsquota_elb_listeners_per_clb{account="123456789",instance="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",region="us-east-1"} 10.0
awsquota_elb_listeners_per_clb{account="123456789",instance="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",region="us-east-1"} 2.0
```

As querying all quotas, depending on the number of resources to check, may take some time, the exporter works asynchronously. That means requesting the /metrics endpoint will return cached results and not trigger a recheck of all quotas. Instead all checks will be executed and refreshed in the background. That's why no metrics will be available directly after starting the exporter.

Hence it doesn't make too much sense to scrape the /metrics every few seconds cause the values will only refresh once in a while. The check intervals of the background jobs can be adjusted to your needs using command line arguments.

## Autocompletion

To enable autocompletion for all check keys, sub commands and their options, follow one of the next sections depending on the shell you use.

### Bash

Add this to your _~/.bashrc_:
`eval "$(_AWS_QUOTA_CHECKER_COMPLETE=source_bash aws-quota-checker)"`

### Zsh

Add this to your _~/.zshrc_:
`eval "$(_AWS_QUOTA_CHECKER_COMPLETE=source_zsh aws-quota-checker)"`

### Fish

Add this to your _~/.config/fish/completions/aws-quota-checker.fish_:
`eval "$(_AWS_QUOTA_CHECKER_COMPLETE=source_fish aws-quota-checker)"`

## Missing a quota check?

Feel free to create a new issue with the _New Check_ label including a description which quota check you are missing.
