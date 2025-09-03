variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "slack_webhook_url" {
  description = "Slack webhook URL for notifications"
  type        = string
  sensitive   = true
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "aws-slack-alerts"
}

variable "cpu_threshold" {
  description = "CPU threshold percentage for CloudWatch alarms"
  type        = number
  default     = 80
}

variable "budget_limit" {
  description = "Budget limit in USD"
  type        = number
  default     = 100
}

variable "budget_email" {
  description = "Email for budget notifications"
  type        = string
}

variable "use_existing_guardduty" {
  description = "Whether to use existing GuardDuty detector (true) or create new one (false)"
  type        = bool
  default     = true
}