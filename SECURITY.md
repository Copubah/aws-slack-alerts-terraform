# Security Policy

## Supported Versions

We support the latest version of this project. Please ensure you're using the most recent release.

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < Latest| :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** create a public GitHub issue
2. Email the maintainer directly at: charles.opuba@example.com
3. Include detailed information about the vulnerability
4. Allow reasonable time for the issue to be addressed

## Security Considerations

This project handles sensitive information including:
- Slack webhook URLs
- AWS credentials and permissions
- Infrastructure monitoring data

### Best Practices

1. **Never commit sensitive data** to the repository
2. Use Terraform variables for all sensitive values
3. Store webhook URLs and credentials securely
4. Follow AWS IAM least privilege principle
5. Regularly rotate credentials and webhook URLs
6. Monitor CloudTrail logs for unusual activity

### AWS Security

- Lambda functions use minimal IAM permissions
- SNS topics have service-specific publish policies
- GuardDuty is enabled for threat detection
- All resources are tagged for tracking

### Slack Security

- Use dedicated webhook URLs for this integration
- Limit webhook permissions to specific channels
- Monitor Slack audit logs for unusual activity
- Consider using Slack's IP allowlisting if available

## Vulnerability Response

When a security issue is reported:

1. We will acknowledge receipt within 48 hours
2. We will provide an initial assessment within 5 business days
3. We will work on a fix and coordinate disclosure
4. We will release a security update as soon as possible
5. We will provide credit to the reporter (if desired)

## Security Updates

Security updates will be:
- Released as soon as possible
- Clearly marked in release notes
- Communicated through GitHub releases
- Include upgrade instructions

Thank you for helping keep this project secure!