#!/usr/bin/env python3
"""
Unit tests for the Lambda function
"""

import json
import pytest
import os
from unittest.mock import patch, MagicMock
from moto import mock_sns
import boto3

# Import the lambda function
import sys
sys.path.append('.')
from lambda_function import lambda_handler, format_slack_message


class TestLambdaFunction:
    
    def test_format_cloudwatch_alarm_message(self):
        """Test CloudWatch alarm message formatting"""
        message = {
            'AlarmName': 'HighCPUAlarm',
            'NewStateValue': 'ALARM',
            'NewStateReason': 'CPU utilization exceeded 80%',
            'Region': 'us-east-1',
            'StateChangeTime': '2024-01-01T12:00:00Z'
        }
        
        result = format_slack_message(message, 'CloudWatch Alarm')
        
        assert result['text'] == '🚨 AWS Alert: CloudWatch Alarm'
        assert len(result['attachments']) == 1
        assert result['attachments'][0]['color'] == 'danger'
        assert result['attachments'][0]['title'] == 'CloudWatch Alarm: HighCPUAlarm'
    
    def test_format_guardduty_message(self):
        """Test GuardDuty finding message formatting"""
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
        
        assert result['text'] == '🚨 AWS Alert: GuardDuty Finding'
        assert len(result['attachments']) == 1
        assert result['attachments'][0]['color'] == 'danger'
        assert 'HIGH' in result['attachments'][0]['fields'][0]['value']
    
    def test_format_ec2_state_change_message(self):
        """Test EC2 state change message formatting"""
        message = {
            'source': 'aws.ec2',
            'detail': {
                'instance-id': 'i-1234567890abcdef0',
                'state': 'running'
            },
            'region': 'us-east-1'
        }
        
        result = format_slack_message(message, 'EC2 State Change')
        
        assert result['text'] == '🚨 AWS Alert: EC2 State Change'
        assert len(result['attachments']) == 1
        assert result['attachments'][0]['color'] == 'good'
        assert result['attachments'][0]['title'] == '🖥️ EC2 Instance State Change'
    
    def test_format_budget_alert_message(self):
        """Test budget alert message formatting"""
        message = {
            'budgetName': 'monthly-budget',
            'thresholdType': 'PERCENTAGE',
            'threshold': 80
        }
        
        result = format_slack_message(message, 'Budget Alert')
        
        assert result['text'] == '🚨 AWS Alert: Budget Alert'
        assert len(result['attachments']) == 1
        assert result['attachments'][0]['color'] == 'warning'
        assert result['attachments'][0]['title'] == '💰 AWS Budget Alert'
    
    @patch('urllib3.PoolManager')
    @patch.dict(os.environ, {'SLACK_WEBHOOK_URL': 'https://hooks.slack.com/test'})
    def test_lambda_handler_success(self, mock_pool_manager):
        """Test successful lambda handler execution"""
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
        
        assert result['statusCode'] == 200
        assert 'successfully' in result['body']
    
    @patch.dict(os.environ, {}, clear=True)
    def test_lambda_handler_missing_webhook_url(self):
        """Test lambda handler with missing webhook URL"""
        event = {
            'Records': [
                {
                    'Sns': {
                        'Subject': 'Test Alert',
                        'Message': json.dumps({'test': 'message'})
                    }
                }
            ]
        }
        
        context = {}
        
        result = lambda_handler(event, context)
        
        assert result['statusCode'] == 500
        assert 'webhook URL not configured' in result['body']
    
    @patch('urllib3.PoolManager')
    @patch.dict(os.environ, {'SLACK_WEBHOOK_URL': 'https://hooks.slack.com/test'})
    def test_lambda_handler_http_error(self, mock_pool_manager):
        """Test lambda handler with HTTP error"""
        # Mock HTTP error
        mock_pool_manager.return_value.request.side_effect = Exception('HTTP Error')
        
        event = {
            'Records': [
                {
                    'Sns': {
                        'Subject': 'Test Alert',
                        'Message': json.dumps({'test': 'message'})
                    }
                }
            ]
        }
        
        context = {}
        
        result = lambda_handler(event, context)
        
        assert result['statusCode'] == 500
        assert 'Error' in result['body']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])