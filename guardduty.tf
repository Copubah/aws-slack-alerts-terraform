# Enable GuardDuty
resource "aws_guardduty_detector" "main" {
  enable = true

  datasources {
    s3_logs {
      enable = true
    }
    kubernetes {
      audit_logs {
        enable = true
      }
    }
    malware_protection {
      scan_ec2_instance_with_findings {
        ebs_volumes {
          enable = true
        }
      }
    }
  }

  tags = {
    Name = "${var.project_name}-guardduty"
  }
}

# GuardDuty Finding Format
resource "aws_guardduty_publishing_destination" "example" {
  count           = 0 # Set to 1 if you want to enable S3 publishing
  detector_id     = aws_guardduty_detector.main.id
  destination_arn = "arn:aws:s3:::example-bucket"
  kms_key_arn     = "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012"

  destination_type = "S3"
}