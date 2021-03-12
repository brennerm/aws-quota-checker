# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- now available as a Docker image, give it a try with `docker run ghcr.io/brennerm/aws-quota-checker:latest`

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
