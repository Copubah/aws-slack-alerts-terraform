import json
import urllib3
import os
from datetime import datetime

def lambda_handler(event, context):
    """
    Lambda function to forward SNS messages to Slack
    """

    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

    if not slack_webhook_url:
        print("ERROR: SLACK_WEBHOOK_URL environment variable not set")
        return {
            'statusCode': 500,
            'body': json.dumps('Slack webhook URL not configured')
        }

    http = urllib3.PoolManager()

    try:
        # Parse SNS message
        for record in event['Records']:
            sns_message = json.loads(record['Sns']['Message'])
            subject = record['Sns']['Subject'] or 'AWS Alert'

            # Determine alert type and format message
            slack_message = format_slack_message(sns_message, subject)

            # Send to Slack
            response = http.request(
                'POST',
                slack_webhook_url,
                body=json.dumps(slack_message),
                headers={'Content-Type': 'application/json'}
            )

            print(f"Slack response: {response.status}")

        return {
            'statusCode': 200,
            'body': json.dumps('Messages sent to Slack successfully')
        }

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

def format_slack_message(message, subject):
    """
    Format different types of AWS alerts for Slack
    """

    # Default message structure
    slack_message = {
        "text": f"🚨 AWS Alert: {subject}",
        "attachments": []
    }

    # CloudWatch Alarm
    if 'AlarmName' in message:
        color = "danger" if message.get('NewStateValue') == 'ALARM' else "good"
        attachment = {
            "color": color,
            "title": f"CloudWatch Alarm: {message['AlarmName']}",
            "fields": [
                {
                    "title": "State",
                    "value": message.get('NewStateValue', 'Unknown'),
                    "short": True
                },
                {
                    "title": "Reason",
                    "value": message.get('NewStateReason', 'No reason provided'),
                    "short": False
                },
                {
                    "title": "Region",
                    "value": message.get('Region', 'Unknown'),
                    "short": True
                },
                {
                    "title": "Timestamp",
                    "value": message.get('StateChangeTime', datetime.now().isoformat()),
                    "short": True
                }
            ]
        }
        slack_message["attachments"].append(attachment)

    # GuardDuty Finding
    elif 'source' in message and message['source'] == 'aws.guardduty':
        detail = message.get('detail', {})
        severity = detail.get('severity', 0)

        if severity >= 7:
            color = "danger"
            severity_text = "HIGH"
        elif severity >= 4:
            color = "warning"
            severity_text = "MEDIUM"
        else:
            color = "good"
            severity_text = "LOW"

        attachment = {
            "color": color,
            "title": f"🛡️ GuardDuty Finding: {detail.get('type', 'Unknown')}",
            "fields": [
                {
                    "title": "Severity",
                    "value": f"{severity_text} ({severity})",
                    "short": True
                },
                {
                    "title": "Description",
                    "value": detail.get('description', 'No description available'),
                    "short": False
                },
                {
                    "title": "Region",
                    "value": message.get('region', 'Unknown'),
                    "short": True
                }
            ]
        }
        slack_message["attachments"].append(attachment)

    # EC2 Instance State Change
    elif 'source' in message and message['source'] == 'aws.ec2':
        detail = message.get('detail', {})
        state = detail.get('state', 'unknown')

        color = "good" if state == "running" else "warning" if state in ["stopping", "stopped"] else "danger"

        attachment = {
            "color": color,
            "title": f"🖥️ EC2 Instance State Change",
            "fields": [
                {
                    "title": "Instance ID",
                    "value": detail.get('instance-id', 'Unknown'),
                    "short": True
                },
                {
                    "title": "State",
                    "value": state.title(),
                    "short": True
                },
                {
                    "title": "Region",
                    "value": message.get('region', 'Unknown'),
                    "short": True
                }
            ]
        }
        slack_message["attachments"].append(attachment)

    # Budget Alert
    elif 'budgetName' in message or 'Budget' in subject:
        attachment = {
            "color": "warning",
            "title": "💰 AWS Budget Alert",
            "fields": [
                {
                    "title": "Alert Type",
                    "value": "Budget Threshold Exceeded",
                    "short": True
                },
                {
                    "title": "Details",
                    "value": str(message),
                    "short": False
                }
            ]
        }
        slack_message["attachments"].append(attachment)

    # Generic message
    else:
        attachment = {
            "color": "warning",
            "title": "AWS Notification",
            "text": json.dumps(message, indent=2)
        }
        slack_message["attachments"].append(attachment)

    return slack_message