# aws-quota-checker

A tool that helps keeping track of your AWS quota utilization. It'll determine the limits of your AWS account and compare them to the number of current resources.

![Example output of aws-quota-checker](/img/example.png)

This is especially useful cause today, cloud resources are being created from all kinds of sources, e.g. IaC and Kubernetes operators. This tool will give you a head start for requesting quota increases before you hit a quota limit to prevent being stuck with a production system not being able to scale anymore.

A usual use case is to add it to your CI pipeline right after applying your IaC or run it on a regular basis. Feel free to leave a vote on [this issue](https://github.com/brennerm/aws-quota-checker/issues/1) if you'd like to see a Prometheus exporter.

## Installation

### From pypi

```bash
pip install aws-quota-checker
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

## Missing a quota check?

Feel free to create a new issue with the _New Check_ label including a description which quota check you are missing.
