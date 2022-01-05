# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- add error handling for CLI result reporter
- new check: iam_role_count
- Prometheus metrics now have a new label that contains the quota key, see [#31](https://github.com/brennerm/aws-quota-checker/issues/31) for further details

## [1.9.0] - 2021-09-21

### Added

- new check: rds_event_subscriptions

### Removed

- obsolete check: cw_alarm_count

## [1.8.0] - 2021-09-10

### Added

- new check: rds_instances
- new check: rds_parameter_groups
- new check: rds_cluster_parameter_groups

### Fixed

- iterator bug that prevented check-instance command to function

### Security

- update several dependencies

## [1.7.0] - 2021-05-05

### Added

- new check: lambda_function_storage

## [1.6.0] - 2021-04-30

### Added

- new check: elb_target_groups_per_alb

### Fixed

- fix wrong number of EBS snapshots

## [1.5.0] - 2021-04-19

### Added

- new check: ses_daily_sends

### Fixed

- upgraded urllib due to [vulnerability CVE-2021-28363](https://github.com/advisories/GHSA-5phf-pp7p-vc2r)

## [1.4.1] - 2021-03-25

### Fixed

- make code compatible with Python 3.7

## [1.4.0] - 2021-03-21

### Added

- new check: vpc_rules_per_acl
- new check: vpc_ipv4_cidr_blocks_per_vpc
- new check: vpc_ipv6_cidr_blocks_per_vpc
- new check: vpc_rules_per_sg
- new check: vpc_route_tables_per_vpc
- new check: vpc_routes_per_route_table
- add Grafana dashboard: on-demand-ec2
- new Prometheus metric that will expose the time it took to get the current/max value of each check

## [1.3.1] - 2021-03-17

### Fixed

- fix check key validation for _check_ and _prometheus-exporter_ subcommands

## [1.3.0] - 2021-03-12

### Added

- now available as a Docker image, give it a try with `docker run ghcr.io/brennerm/aws-quota-checker:latest`
- improve autocompletion support

## [1.2.0] - 2021-03-09

### Added

- implement Prometheus exporter that provides access to all quota results

### Changed

- display AWS account ID instead of profile name in check scope

## [1.1.0] - 2021-02-27

### Added

- new check: ec2_on_demand_f_count
- new check: ec2_on_demand_g_count
- new check: ec2_on_demand_p_count
- new check: ec2_on_demand_x_count
- new check: ec2_on_demand_inf_count
- new check: ec2_spot_f_count
- new check: ec2_spot_g_count
- new check: ec2_spot_p_count
- new check: ec2_spot_x_count
- new check: ec2_spot_inf_count
- new check: sns_topics_count
- new check: sns_pending_subscriptions_count
- new check: sns_subscriptions_per_topic

### Changed

- sort checks alphabetically by key

## [1.0.0] - 2021-02-24

### Added

- initial release
