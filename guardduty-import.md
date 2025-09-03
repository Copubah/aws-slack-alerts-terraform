# GuardDuty Import Guide

## Issue
GuardDuty detector already exists in your AWS account, causing Terraform to fail when trying to create a new one.

## Solution Options

### Option 1: Use Existing GuardDuty (Current Configuration)
The current configuration uses a data source to reference the existing GuardDuty detector. This is the safest approach.

### Option 2: Import Existing GuardDuty into Terraform
If you want Terraform to manage your existing GuardDuty detector:

1. **Find your GuardDuty detector ID:**
   ```bash
   aws guardduty list-detectors --region us-east-1
   ```

2. **Import the existing detector:**
   ```bash
   # Replace DETECTOR_ID with your actual detector ID
   terraform import aws_guardduty_detector.main DETECTOR_ID
   ```

3. **Uncomment the GuardDuty resource in guardduty.tf:**
   ```hcl
   resource "aws_guardduty_detector" "main" {
     enable = true
     # ... rest of configuration
   }
   ```

4. **Update the configuration to match your existing settings:**
   ```bash
   terraform plan
   # Review the changes and adjust the configuration as needed
   ```

### Option 3: Manage GuardDuty Separately
Keep GuardDuty managed outside of Terraform and only use the data source (current approach).

## Current Status
- ✅ EventBridge rules will work with existing GuardDuty
- ✅ GuardDuty findings will be routed to SNS/Slack
- ✅ No changes needed to existing GuardDuty configuration

## Recommendation
Use the current configuration (Option 1) unless you specifically need Terraform to manage GuardDuty settings.