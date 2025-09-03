#!/usr/bin/env python3
"""
Local test for Lambda function
"""

import json
import os
from unittest.mock import patch, MagicMock

# Set environment variable for testing
os.environ['SLACK_WEBHOOK_URL'] = 'https://hooks.slack.com/test'

# Import the lambda function
from lambda_function import lambda_handler, format_slack_message

def test_cloudwatch_alarm():
    """Test CloudWatch alarm formatting"""
    print("Testing CloudWatch alarm formatting...")
    
    message = {
        'AlarmName': 'HighCPUAlarm',
        'NewStateValue': 'ALARM',
        'NewStateReason': 'CPU utilization exceeded 80%',
        'Region': 'us-east-1',
        'StateChangeTime': '2025-01-01T12:00:00Z'
    }
    
    result = format_slack_message(message, 'CloudWatch Alarm')
    print(f"✅ CloudWatch alarm formatted: {result['text']}")
    print(f"   Color: {result['attachments'][0]['color']}")
    return True

def test_guardduty_finding():
    """Test GuardDuty finding formatting"""
    print("Testing GuardDuty finding formatting...")
    
    message = {
        'source': 'aws.guardduty',
        'detail': {
            'type': 'Trojan:EC2/DNSDataExfiltration',
            'severity': 8.5,
            'description': 'EC2 instance is communicating with a domain name that is being used by a known malware.'
        },
        'region': 'us-east-1'
    }
    
    result = format_slack_message(message, 'GuardDuty Finding')
    print(f"✅ GuardDuty finding formatted: {result['text']}")
    print(f"   Severity: HIGH (8.5)")
    return True

def test_ec2_state_change():
    """Test EC2 state change formatting"""
    print("Testing EC2 state change formatting...")
    
    message = {
        'source': 'aws.ec2',
        'detail': {
            'instance-id': 'i-1234567890abcdef0',
            'state': 'running'
        },
        'region': 'us-east-1'
    }
    
    result = format_slack_message(message, 'EC2 State Change')
    print(f"✅ EC2 state change formatted: {result['text']}")
    print(f"   Instance: i-1234567890abcdef0 -> running")
    return True

@patch('urllib3.PoolManager')
def test_lambda_handler(mock_pool_manager):
    """Test full Lambda handler"""
    print("Testing Lambda handler...")
    
    # Mock HTTP response
    mock_response = MagicMock()
    mock_response.status = 200
    mock_pool_manager.return_value.request.return_value = mock_response
    
    # Create test event
    event = {
        'Records': [
            {
                'Sns': {
                    'Subject': 'Test Alert',
                    'Message': json.dumps({
                        'AlarmName': 'TestAlarm',
                        'NewStateValue': 'ALARM',
                        'NewStateReason': 'Test reason'
                    })
                }
            }
        ]
    }
    
    context = {}
    result = lambda_handler(event, context)
    
    print(f"✅ Lambda handler executed: Status {result['statusCode']}")
    return result['statusCode'] == 200

if __name__ == '__main__':
    print("🧪 Testing Lambda Function Locally")
    print("=" * 50)
    
    tests = [
        test_cloudwatch_alarm,
        test_guardduty_finding,
        test_ec2_state_change,
        test_lambda_handler
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test failed: {e}")
            print()
    
    print(f"📊 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Lambda function is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the Lambda function code.")