# AWS Slack Alerts Terraform Project

**Author:** Charles Opuba

This Terraform project creates a comprehensive AWS monitoring and alerting system that sends notifications to Slack. It integrates multiple AWS services to provide real-time alerts for various events and metrics.

## Features

- **SNS Topic**: Central hub for all alerts
- **Lambda Function**: Processes and formats messages for Slack
- **CloudWatch Alarms**: Monitors EC2 CPU usage and Lambda performance
- **GuardDuty Integration**: Security findings alerts
- **EventBridge Rules**: Captures EC2, Auto Scaling, and RDS events
- **Budget Alerts**: Cost monitoring and notifications
- **IAM Roles**: Proper permissions for all services

## Architecture

```
See architecture.txt for detailed ASCII diagram
```

The system follows this flow:
```
AWS Services → EventBridge/CloudWatch → SNS Topic → Lambda → Slack
```

### Components:
- **AWS Services**: EC2, RDS, Auto Scaling, GuardDuty generate events
- **EventBridge**: Routes service events to SNS
- **CloudWatch**: Monitors metrics and triggers alarms
- **SNS Topic**: Central hub for all notifications
- **Lambda Function**: Processes and formats messages for Slack
- **Slack**: Receives formatted notifications

## Prerequisites

1. **Terraform** >= 1.0
2. **AWS CLI** configured with appropriate permissions
3. **Slack Webhook URL** - Create a Slack app and get the webhook URL

### Setting up Slack Webhook

1. Go to https://api.slack.com/apps
2. Create a new app or use existing one
3. Go to "Incoming Webhooks" and activate them
4. Create a new webhook for your desired channel
5. Copy the webhook URL

## Quick Start

1. **Clone and configure**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values
   ```

2. **Initialize and deploy**:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

3. **Test the integration**:
   ```bash
   # Trigger a test notification
   aws sns publish \
     --topic-arn $(terraform output -raw sns_topic_arn) \
     --subject "Test Alert" \
     --message "This is a test message from AWS"
   ```

## Configuration

### Required Variables

- `slack_webhook_url`: Your Slack webhook URL (sensitive)
- `budget_email`: Email for budget notifications

### Optional Variables

- `aws_region`: AWS region (default: us-east-1)
- `environment`: Environment name (default: dev)
- `project_name`: Project name for resources (default: aws-slack-alerts)
- `cpu_threshold`: CPU alarm threshold (default: 80%)
- `budget_limit`: Monthly budget limit in USD (default: 100)

## Monitoring Coverage

### CloudWatch Alarms
- EC2 High CPU utilization
- Lambda function errors
- Lambda function duration

### EventBridge Rules
- GuardDuty security findings
- EC2 instance state changes
- Auto Scaling events
- RDS database events

### Budget Alerts
- 80% of budget threshold (actual)
- 100% of budget threshold (forecasted)

## Slack Message Formats

The Lambda function formats different alert types:

- **CloudWatch Alarms**: Shows alarm name, state, reason, and timestamp
- **GuardDuty Findings**: Displays severity, description, and affected resources
- **EC2 Events**: Instance ID, state changes, and region
- **Budget Alerts**: Cost threshold notifications
- **Generic Events**: Formatted JSON for other AWS events

## Customization

### Adding New Alarms

Add CloudWatch alarms in `cloudwatch.tf`:

```hcl
resource "aws_cloudwatch_metric_alarm" "custom_alarm" {
  alarm_name          = "custom-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "YourMetric"
  namespace           = "AWS/YourService"
  period              = "300"
  statistic           = "Average"
  threshold           = "10"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}
```

### Adding New EventBridge Rules

Add rules in `events.tf`:

```hcl
resource "aws_cloudwatch_event_rule" "custom_rule" {
  name = "custom-rule"
  event_pattern = jsonencode({
    source = ["aws.yourservice"]
    detail-type = ["Your Event Type"]
  })
}

resource "aws_cloudwatch_event_target" "custom_target" {
  rule      = aws_cloudwatch_event_rule.custom_rule.name
  target_id = "CustomToSNS"
  arn       = aws_sns_topic.alerts.arn
}
```

## Security Considerations

- Lambda function has minimal IAM permissions
- SNS topic has service-specific publish permissions
- Slack webhook URL is marked as sensitive
- GuardDuty is enabled with comprehensive data sources

## Costs

Estimated monthly costs (us-east-1):
- SNS: ~$0.50 (1000 notifications)
- Lambda: ~$0.20 (1000 invocations)
- CloudWatch: ~$0.30 (alarms)
- GuardDuty: ~$4.00 (base cost)
- EventBridge: ~$1.00 (custom rules)

**Total: ~$6.00/month**

## Troubleshooting

### Lambda Function Issues
```bash
# Check Lambda logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/aws-slack-alerts"
aws logs tail "/aws/lambda/aws-slack-alerts-slack-notifier" --follow
```

### SNS Topic Issues
```bash
# Test SNS topic
aws sns publish --topic-arn YOUR_TOPIC_ARN --subject "Test" --message "Test message"
```

### EventBridge Issues
```bash
# List EventBridge rules
aws events list-rules --name-prefix "aws-slack-alerts"
```

## Cleanup

```bash
terraform destroy
```

## CI/CD Pipeline

This project includes a comprehensive CI/CD pipeline with GitHub Actions:

### 🔄 **Continuous Integration**
- **Terraform Validation**: Format checking, validation, and planning
- **Security Scanning**: Automated security analysis with Checkov
- **Lambda Testing**: Unit tests for Python Lambda function
- **Documentation Validation**: Link checking and content validation

### 🚀 **Continuous Deployment**
- **Multi-Environment Support**: Deploy to dev, staging, and prod
- **Infrastructure as Code**: Automated Terraform deployments
- **Drift Detection**: Daily checks for infrastructure drift
- **Cost Monitoring**: Weekly cost analysis and optimization reports

### 📊 **Monitoring & Maintenance**
- **Automated Releases**: Tag-based release automation
- **Cost Optimization**: Unused resource detection
- **Security Monitoring**: Continuous security scanning
- **Performance Tracking**: Lambda function performance monitoring

### Environment Configuration

The project supports multiple environments with different configurations:

```bash
# Development
environments/dev/terraform.tfvars.example

# Staging  
environments/staging/terraform.tfvars.example

# Production
environments/prod/terraform.tfvars.example
```

### GitHub Secrets Required

Configure these secrets in your GitHub repository:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

# Application Configuration
SLACK_WEBHOOK_URL
BUDGET_EMAIL
```

### GitHub Variables

Configure these variables for your environments:

```bash
# Infrastructure
TF_STATE_BUCKET=your-terraform-state-bucket
TF_LOCK_TABLE=your-terraform-lock-table
AWS_REGION=us-east-1

# Application
PROJECT_NAME=aws-slack-alerts
CPU_THRESHOLD=80
BUDGET_LIMIT=100
```

### Deployment Commands

```bash
# Deploy to development
gh workflow run cd-deploy.yml -f environment=dev

# Deploy to production
gh workflow run cd-deploy.yml -f environment=prod

# Destroy infrastructure
gh workflow run cd-deploy.yml -f environment=dev -f destroy=true
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes following the coding standards
4. Run tests: `python -m pytest tests/ -v`
5. Ensure CI passes: All GitHub Actions workflows must pass
6. Submit a pull request with detailed description

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed release notes and version history.

## License

MIT License - see [LICENSE](LICENSE) file for details.
## Architecture Diagram

The system architecture is documented in `architecture.txt` with a detailed ASCII diagram showing all components and data flows.

For a visual diagram, you can optionally generate one using:

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate diagram
python architecture.py
```

---

**Created by Charles Opuba** | [GitHub](https://github.com/Copubah) | [LinkedIn](https://www.linkedin.com/in/charles-opuba-94820574/)