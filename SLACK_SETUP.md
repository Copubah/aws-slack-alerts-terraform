# Slack App Setup Guide

## Step 1: Create or Configure Your Slack App

### Option A: Create New Slack App
1. Go to https://api.slack.com/apps
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. Enter app name: `AWS Alerts` (or your preferred name)
5. Select your Slack workspace
6. Click **"Create App"**

### Option B: Use Existing Slack App
1. Go to https://api.slack.com/apps
2. Select your existing app
3. Continue to Step 2

## Step 2: Enable Incoming Webhooks

1. In your app settings, click **"Incoming Webhooks"** in the left sidebar
2. Toggle **"Activate Incoming Webhooks"** to **ON**
3. Click **"Add New Webhook to Workspace"**
4. Select the channel where you want alerts (e.g., `#aws-alerts`, `#monitoring`)
5. Click **"Allow"**

## Step 3: Copy Your Webhook URL

1. You'll see your webhook URL in this format:
   ```
   https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
   ```
2. **Copy this URL** - you'll need it for Terraform

## Step 4: Test Your Webhook

### Quick Test (Replace with your actual URL):
```bash
python quick_slack_test.py "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### Interactive Test:
```bash
python test_slack_integration.py
```

## Step 5: Configure Terraform

1. **Update terraform.tfvars:**
   ```hcl
   slack_webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
   budget_email = "your-email@example.com"
   ```

2. **Or set environment variable:**
   ```bash
   export TF_VAR_slack_webhook_url="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
   ```

## Step 6: Deploy Infrastructure

```bash
terraform plan
terraform apply
```

## Step 7: Test AWS Integration

After deployment, test with a real AWS event:
```bash
# Get your SNS topic ARN
SNS_TOPIC_ARN=$(terraform output -raw sns_topic_arn)

# Send test message
aws sns publish \
  --topic-arn "$SNS_TOPIC_ARN" \
  --subject "Test Alert" \
  --message '{"AlarmName":"TestAlarm","NewStateValue":"ALARM","NewStateReason":"This is a test"}'
```

## Message Examples

Your Slack channel will receive formatted messages like:

### CloudWatch Alarm
```
🚨 AWS Alert: CloudWatch Alarm
┌─────────────────────────────────┐
│ CloudWatch Alarm: HighCPUAlarm │
│ State: ALARM                    │
│ Reason: CPU exceeded 80%        │
│ Region: us-east-1              │
└─────────────────────────────────┘
```

### GuardDuty Finding
```
🚨 AWS Alert: GuardDuty Finding
┌─────────────────────────────────────┐
│ 🛡️ GuardDuty: Trojan:EC2/Malware   │
│ Severity: HIGH (8.5)                │
│ Description: Malware detected...    │
└─────────────────────────────────────┘
```

### EC2 State Change
```
🚨 AWS Alert: EC2 State Change
┌─────────────────────────────────┐
│ 🖥️ EC2 Instance State Change    │
│ Instance: i-1234567890abcdef0   │
│ State: Running                  │
└─────────────────────────────────┘
```

## Troubleshooting

### Common Issues:

1. **"Invalid webhook URL"**
   - Ensure URL starts with `https://hooks.slack.com/services/`
   - Check that webhook is active in Slack app settings

2. **"Channel not found"**
   - Verify the app has permission to post to the channel
   - Re-add webhook to workspace if needed

3. **"No messages appearing"**
   - Check if webhook URL is correct in terraform.tfvars
   - Verify Lambda function has the right environment variable
   - Check CloudWatch logs for Lambda errors

4. **"Messages not formatted"**
   - This is normal - the Lambda function will format them properly
   - Test messages may look different from actual AWS alerts

### Verification Commands:

```bash
# Check Lambda environment variables
aws lambda get-function-configuration \
  --function-name aws-slack-alerts-slack-notifier \
  --query 'Environment.Variables'

# Check SNS topic
aws sns list-subscriptions-by-topic \
  --topic-arn $(terraform output -raw sns_topic_arn)

# Check Lambda logs
aws logs tail "/aws/lambda/aws-slack-alerts-slack-notifier" --follow
```

## Security Notes

- ✅ Keep webhook URL secret (it's marked as sensitive in Terraform)
- ✅ Use environment-specific webhooks for dev/staging/prod
- ✅ Regularly rotate webhook URLs if compromised
- ✅ Monitor Slack audit logs for unusual activity

## Next Steps

Once your Slack integration is working:
1. ✅ Deploy to additional environments (staging, prod)
2. ✅ Customize alert formatting in `lambda_function.py`
3. ✅ Add more AWS services to monitor
4. ✅ Set up alert escalation rules
5. ✅ Create Slack workflows for incident response