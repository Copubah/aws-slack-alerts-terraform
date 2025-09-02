# EventBridge Rule for GuardDuty Findings
resource "aws_cloudwatch_event_rule" "guardduty_findings" {
  name        = "${var.project_name}-guardduty-findings"
  description = "Capture GuardDuty findings"

  event_pattern = jsonencode({
    source      = ["aws.guardduty"]
    detail-type = ["GuardDuty Finding"]
  })

  tags = {
    Name = "${var.project_name}-guardduty-rule"
  }
}

# EventBridge Target for GuardDuty
resource "aws_cloudwatch_event_target" "guardduty_sns" {
  rule      = aws_cloudwatch_event_rule.guardduty_findings.name
  target_id = "GuardDutyToSNS"
  arn       = aws_sns_topic.alerts.arn
}

# EventBridge Rule for EC2 Instance State Changes
resource "aws_cloudwatch_event_rule" "ec2_state_change" {
  name        = "${var.project_name}-ec2-state-change"
  description = "Capture EC2 instance state changes"

  event_pattern = jsonencode({
    source      = ["aws.ec2"]
    detail-type = ["EC2 Instance State-change Notification"]
    detail = {
      state = ["running", "stopped", "terminated", "stopping"]
    }
  })

  tags = {
    Name = "${var.project_name}-ec2-state-rule"
  }
}

# EventBridge Target for EC2 State Changes
resource "aws_cloudwatch_event_target" "ec2_state_sns" {
  rule      = aws_cloudwatch_event_rule.ec2_state_change.name
  target_id = "EC2StateToSNS"
  arn       = aws_sns_topic.alerts.arn
}

# EventBridge Rule for Auto Scaling Events
resource "aws_cloudwatch_event_rule" "autoscaling_events" {
  name        = "${var.project_name}-autoscaling-events"
  description = "Capture Auto Scaling events"

  event_pattern = jsonencode({
    source = ["aws.autoscaling"]
    detail-type = [
      "EC2 Instance Launch Successful",
      "EC2 Instance Launch Unsuccessful",
      "EC2 Instance Terminate Successful",
      "EC2 Instance Terminate Unsuccessful"
    ]
  })

  tags = {
    Name = "${var.project_name}-autoscaling-rule"
  }
}

# EventBridge Target for Auto Scaling Events
resource "aws_cloudwatch_event_target" "autoscaling_sns" {
  rule      = aws_cloudwatch_event_rule.autoscaling_events.name
  target_id = "AutoScalingToSNS"
  arn       = aws_sns_topic.alerts.arn
}

# EventBridge Rule for RDS Events
resource "aws_cloudwatch_event_rule" "rds_events" {
  name        = "${var.project_name}-rds-events"
  description = "Capture RDS events"

  event_pattern = jsonencode({
    source = ["aws.rds"]
    detail-type = [
      "RDS DB Instance Event",
      "RDS DB Cluster Event"
    ]
  })

  tags = {
    Name = "${var.project_name}-rds-rule"
  }
}

# EventBridge Target for RDS Events
resource "aws_cloudwatch_event_target" "rds_sns" {
  rule      = aws_cloudwatch_event_rule.rds_events.name
  target_id = "RDSToSNS"
  arn       = aws_sns_topic.alerts.arn
}