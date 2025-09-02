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

![Architecture Diagram](architecture.png)

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
##
 Architecture Diagram Generation

To generate the architecture diagram:

```bash
# Install required Python packages
pip install diagrams

# Generate the diagram
python architecture.py
```

This will create `architecture.png` showing the complete system architecture.

---

**Created by Charles Opuba** | [GitHub](https://github.com/charlesopuba) | [LinkedIn](https://linkedin.com/in/charlesopuba)