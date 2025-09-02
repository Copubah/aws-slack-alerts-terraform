output "sns_topic_arn" {
  description = "ARN of the SNS topic for alerts"
  value       = aws_sns_topic.alerts.arn
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.slack_notifier.function_name
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.slack_notifier.arn
}

output "guardduty_detector_id" {
  description = "ID of the GuardDuty detector"
  value       = aws_guardduty_detector.main.id
}

output "cloudwatch_alarms" {
  description = "List of CloudWatch alarm names"
  value = [
    aws_cloudwatch_metric_alarm.high_cpu.alarm_name,
    aws_cloudwatch_metric_alarm.lambda_errors.alarm_name,
    aws_cloudwatch_metric_alarm.lambda_duration.alarm_name
  ]
}

output "eventbridge_rules" {
  description = "List of EventBridge rule names"
  value = [
    aws_cloudwatch_event_rule.guardduty_findings.name,
    aws_cloudwatch_event_rule.ec2_state_change.name,
    aws_cloudwatch_event_rule.autoscaling_events.name,
    aws_cloudwatch_event_rule.rds_events.name
  ]
}