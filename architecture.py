#!/usr/bin/env python3
"""
Generate architecture diagram for AWS Slack Alerts project
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SNS, Eventbridge
from diagrams.aws.monitoring import Cloudwatch
from diagrams.aws.security import GuardDuty
from diagrams.aws.management import Budgets
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.compute import AutoScaling
from diagrams.onprem.chat import Slack

def create_architecture_diagram():
    with Diagram("AWS Slack Alerts Architecture", show=False, direction="TB", filename="architecture"):
        
        # Slack endpoint
        slack = Slack("Slack Channel")
        
        with Cluster("AWS Account"):
            # Core notification infrastructure
            with Cluster("Notification Pipeline"):
                sns_topic = SNS("SNS Topic\n(aws-slack-alerts)")
                lambda_func = Lambda("Lambda Function\n(Slack Notifier)")
                
            # Monitoring services
            with Cluster("Monitoring & Security"):
                cloudwatch = Cloudwatch("CloudWatch\nAlarms")
                guardduty = GuardDuty("GuardDuty\nDetector")
                budgets = Budgets("AWS Budgets")
                eventbridge = Eventbridge("EventBridge\nRules")
            
            # AWS Services being monitored
            with Cluster("Monitored Services"):
                ec2 = EC2("EC2 Instances")
                rds = RDS("RDS Databases")
                autoscaling = AutoScaling("Auto Scaling\nGroups")
        
        # Data flow connections
        cloudwatch >> Edge(label="Alarm States") >> sns_topic
        guardduty >> Edge(label="Security Findings") >> eventbridge
        eventbridge >> Edge(label="Filtered Events") >> sns_topic
        budgets >> Edge(label="Cost Alerts") >> sns_topic
        
        # Service events to EventBridge
        ec2 >> Edge(label="State Changes") >> eventbridge
        rds >> Edge(label="DB Events") >> eventbridge
        autoscaling >> Edge(label="Scaling Events") >> eventbridge
        
        # SNS to Lambda to Slack
        sns_topic >> Edge(label="Trigger") >> lambda_func
        lambda_func >> Edge(label="Formatted Messages") >> slack

if __name__ == "__main__":
    create_architecture_diagram()
    print("Architecture diagram generated as 'architecture.png'")