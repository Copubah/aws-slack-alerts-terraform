# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive CI/CD pipeline with GitHub Actions
- Multi-environment support (dev, staging, prod)
- Infrastructure drift detection
- Cost monitoring and optimization workflows
- Automated testing for Lambda functions
- Security scanning with Checkov
- Documentation validation
- Release automation

### Changed
- Enhanced Terraform validation workflow
- Improved project structure with environment-specific configurations

### Security
- Added security policy and vulnerability reporting guidelines
- Implemented automated security scanning

## [1.0.0] - 2025-02-09

### Added
- Initial release of AWS Slack Alerts Terraform project
- SNS topic for centralized alert management
- Lambda function with intelligent Slack message formatting
- CloudWatch alarms for EC2 CPU, Lambda errors, and duration
- GuardDuty integration for security findings
- EventBridge rules for AWS service events
- AWS Budget alerts for cost monitoring
- Comprehensive documentation and architecture diagrams
- IAM roles with least privilege permissions

### Features
- Multi-service AWS monitoring integration
- Smart Slack message formatting based on alert type
- Cost-effective architecture (~$6/month)
- Security-first approach with GuardDuty
- Comprehensive event coverage (EC2, RDS, Auto Scaling)

### Documentation
- Detailed README with setup instructions
- ASCII architecture diagram
- Contributing guidelines
- Security policy
- MIT license