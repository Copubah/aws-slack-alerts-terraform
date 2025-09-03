#!/usr/bin/env python3
"""
Test Slack integration with your actual Slack app
"""

import json
import urllib3
import os

def test_slack_webhook(webhook_url, test_message=None):
    """
    Test sending a message to your Slack app
    """
    if not webhook_url or webhook_url == "https://hooks.slack.com/test":
        print("❌ Please provide your actual Slack webhook URL")
        print("   Get it from: https://api.slack.com/apps -> Your App -> Incoming Webhooks")
        return False
    
    http = urllib3.PoolManager()
    
    # Default test message
    if not test_message:
        test_message = {
            "text": "🧪 Test Message from AWS Slack Alerts",
            "attachments": [
                {
                    "color": "good",
                    "title": "✅ Integration Test Successful",
                    "fields": [
                        {
                            "title": "Status",
                            "value": "Your AWS Slack Alerts system is working!",
                            "short": False
                        },
                        {
                            "title": "Test Time",
                            "value": "2025-01-09 (Local Test)",
                            "short": True
                        },
                        {
                            "title": "Author",
                            "value": "Charles Opuba",
                            "short": True
                        }
                    ],
                    "footer": "AWS Slack Alerts - Terraform Project"
                }
            ]
        }
    
    try:
        print(f"🚀 Sending test message to Slack...")
        print(f"   Webhook URL: {webhook_url[:50]}...")
        
        response = http.request(
            'POST',
            webhook_url,
            body=json.dumps(test_message),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status == 200:
            print("✅ SUCCESS! Message sent to Slack successfully!")
            print("   Check your Slack channel for the test message.")
            return True
        else:
            print(f"❌ FAILED! HTTP Status: {response.status}")
            print(f"   Response: {response.data.decode('utf-8')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_aws_alert_formats(webhook_url):
    """
    Test different AWS alert message formats
    """
    print("\n🧪 Testing different AWS alert formats...")
    
    # Test CloudWatch Alarm
    cloudwatch_message = {
        "text": "🚨 AWS Alert: CloudWatch Alarm",
        "attachments": [
            {
                "color": "danger",
                "title": "CloudWatch Alarm: HighCPUAlarm",
                "fields": [
                    {
                        "title": "State",
                        "value": "ALARM",
                        "short": True
                    },
                    {
                        "title": "Reason",
                        "value": "CPU utilization exceeded 80%",
                        "short": False
                    },
                    {
                        "title": "Region",
                        "value": "us-east-1",
                        "short": True
                    }
                ]
            }
        ]
    }
    
    # Test GuardDuty Finding
    guardduty_message = {
        "text": "🚨 AWS Alert: GuardDuty Security Finding",
        "attachments": [
            {
                "color": "danger",
                "title": "🛡️ GuardDuty Finding: Trojan:EC2/DNSDataExfiltration",
                "fields": [
                    {
                        "title": "Severity",
                        "value": "HIGH (8.5)",
                        "short": True
                    },
                    {
                        "title": "Description",
                        "value": "EC2 instance is communicating with a domain name that is being used by a known malware.",
                        "short": False
                    }
                ]
            }
        ]
    }
    
    # Test EC2 State Change
    ec2_message = {
        "text": "🚨 AWS Alert: EC2 Instance State Change",
        "attachments": [
            {
                "color": "good",
                "title": "🖥️ EC2 Instance State Change",
                "fields": [
                    {
                        "title": "Instance ID",
                        "value": "i-1234567890abcdef0",
                        "short": True
                    },
                    {
                        "title": "State",
                        "value": "Running",
                        "short": True
                    }
                ]
            }
        ]
    }
    
    messages = [
        ("CloudWatch Alarm", cloudwatch_message),
        ("GuardDuty Finding", guardduty_message),
        ("EC2 State Change", ec2_message)
    ]
    
    success_count = 0
    for name, message in messages:
        print(f"\n📤 Sending {name} test...")
        if test_slack_webhook(webhook_url, message):
            success_count += 1
        
        # Small delay between messages
        import time
        time.sleep(2)
    
    print(f"\n📊 Results: {success_count}/{len(messages)} message types sent successfully")
    return success_count == len(messages)

def main():
    print("🔗 Slack Integration Tester")
    print("=" * 50)
    
    # Get webhook URL from user
    webhook_url = input("Enter your Slack webhook URL: ").strip()
    
    if not webhook_url:
        print("❌ No webhook URL provided. Exiting.")
        return
    
    # Validate webhook URL format
    if not webhook_url.startswith("https://hooks.slack.com/"):
        print("⚠️  Warning: This doesn't look like a Slack webhook URL")
        print("   Expected format: https://hooks.slack.com/services/...")
        
        confirm = input("Continue anyway? (y/N): ").strip().lower()
        if confirm != 'y':
            return
    
    print(f"\n🎯 Testing connection to your Slack app...")
    
    # Test basic connection
    if test_slack_webhook(webhook_url):
        print("\n🎉 Basic test successful! Now testing AWS alert formats...")
        
        # Test different message formats
        if test_aws_alert_formats(webhook_url):
            print("\n✅ ALL TESTS PASSED!")
            print("   Your Slack app is ready to receive AWS alerts!")
            print("\n📝 Next steps:")
            print("   1. Update your terraform.tfvars with this webhook URL")
            print("   2. Deploy your infrastructure: terraform apply")
            print("   3. Your AWS alerts will appear in Slack!")
        else:
            print("\n⚠️  Some message formats failed, but basic connection works")
    else:
        print("\n❌ Connection test failed. Please check:")
        print("   1. Webhook URL is correct")
        print("   2. Slack app has Incoming Webhooks enabled")
        print("   3. Webhook is active and not expired")

if __name__ == '__main__':
    main()