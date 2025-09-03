# Use existing GuardDuty detector
data "aws_guardduty_detector" "existing" {
  # This will find the existing GuardDuty detector in the account
}

# Note: GuardDuty detector already exists in your AWS account
# The EventBridge rules will work with the existing detector
# If you want to manage GuardDuty settings via Terraform, you can:
# 1. Import the existing detector: terraform import aws_guardduty_detector.main <detector-id>
# 2. Or manage it separately from this Terraform configuration

locals {
  guardduty_detector_id = data.aws_guardduty_detector.existing.id
}

# GuardDuty Finding Format (optional S3 publishing)
# Uncomment and configure if you want to publish findings to S3
# resource "aws_guardduty_publishing_destination" "example" {
#   detector_id     = data.aws_guardduty_detector.existing.id
#   destination_arn = "arn:aws:s3:::your-guardduty-findings-bucket"
#   kms_key_arn     = "arn:aws:kms:${var.aws_region}:${data.aws_caller_identity.current.account_id}:key/your-kms-key-id"
#   destination_type = "S3"
# }

# Get current AWS account ID for reference
data "aws_caller_identity" "current" {}