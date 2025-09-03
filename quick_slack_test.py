#!/usr/bin/env python3
"""
Quick test to send a message to your Slack app
Usage: python quick_slack_test.py "your-webhook-url"
"""

import json
import urllib3
import sys

def send_test_message(webhook_url):
    """Send a simple test message to Slack"""
    
    message = {
        "text": "🎉 Hello from AWS Slack Alerts!",
        "attachments": [
            {
                "color": "good",
                "title": "✅ Connection Test Successful",
                "text": "Your Slack integration is working perfectly!",
                "fields": [
                    {
                        "title": "Project",
                        "value": "AWS Slack Alerts Terraform",
                        "short": True
                    },
                    {
                        "title": "Author",
                        "value": "Charles Opuba",
                        "short": True
                    }
                ],
                "footer": "Terraform Infrastructure Project",
                "ts": 1704844800  # Timestamp
            }
        ]
    }
    
    http = urllib3.PoolManager()
    
    try:
        response = http.request(
            'POST',
            webhook_url,
            body=json.dumps(message),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status == 200:
            print("✅ SUCCESS! Check your Slack channel for the message!")
            return True
        else:
            print(f"❌ Failed with status {response.status}: {response.data.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python quick_slack_test.py 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'")
        sys.exit(1)
    
    webhook_url = sys.argv[1]
    print(f"🚀 Sending test message to Slack...")
    send_test_message(webhook_url)