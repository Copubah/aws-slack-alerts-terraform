# Deployment Guide

This guide covers deploying the AWS Slack Alerts infrastructure across different environments using the CI/CD pipeline.

## Prerequisites

### 1. AWS Setup
- AWS account with appropriate permissions
- S3 bucket for Terraform state storage
- DynamoDB table for state locking
- IAM user/role with required permissions

### 2. GitHub Setup
- Fork or clone the repository
- Configure GitHub secrets and variables
- Enable GitHub Actions

### 3. Slack Setup
- Create Slack app and webhook URLs for each environment
- Configure appropriate channels for alerts

## Environment Setup

### Development Environment

1. **Create AWS Resources**:
   ```bash
   # Create S3 bucket for state
   aws s3 mb s3://your-terraform-state-dev --region us-east-1

   # Create DynamoDB table for locking
   aws dynamodb create-table \
     --table-name terraform-lock-dev \
     --attribute-definitions AttributeName=LockID,AttributeType=S \
     --key-schema AttributeName=LockID,KeyType=HASH \
     --billing-mode PAY_PER_REQUEST
   ```

2. **Configure GitHub Variables**:
   ```bash
   # Repository variables
   TF_STATE_BUCKET=your-terraform-state-dev
   TF_LOCK_TABLE=terraform-lock-dev
   AWS_REGION=us-east-1
   PROJECT_NAME=aws-slack-alerts
   CPU_THRESHOLD=90
   BUDGET_LIMIT=50
   ```

3. **Configure GitHub Secrets**:
   ```bash
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/DEV/WEBHOOK
   BUDGET_EMAIL=dev-alerts@example.com
   ```

### Production Environment

1. **Create Production AWS Resources**:
   ```bash
   # Create S3 bucket for state
   aws s3 mb s3://your-terraform-state-prod --region us-east-1

   # Enable versioning and encryption
   aws s3api put-bucket-versioning \
     --bucket your-terraform-state-prod \
     --versioning-configuration Status=Enabled

   aws s3api put-bucket-encryption \
     --bucket your-terraform-state-prod \
     --server-side-encryption-configuration '{
       "Rules": [{
         "ApplyServerSideEncryptionByDefault": {
           "SSEAlgorithm": "AES256"
         }
       }]
     }'

   # Create DynamoDB table for locking
   aws dynamodb create-table \
     --table-name terraform-lock-prod \
     --attribute-definitions AttributeName=LockID,AttributeType=S \
     --key-schema AttributeName=LockID,KeyType=HASH \
     --billing-mode PAY_PER_REQUEST
   ```

2. **Configure Production Environment in GitHub**:
   - Go to Settings > Environments
   - Create "prod" environment
   - Add protection rules (require reviews, restrict to main branch)
   - Configure environment-specific secrets and variables

## Deployment Methods

### 1. Automated Deployment (Recommended)

#### Deploy via GitHub Actions UI:
1. Go to Actions tab in GitHub
2. Select "CD - Deploy to AWS" workflow
3. Click "Run workflow"
4. Select environment and options
5. Monitor deployment progress

#### Deploy via GitHub CLI:
```bash
# Deploy to development
gh workflow run cd-deploy.yml -f environment=dev

# Deploy to staging
gh workflow run cd-deploy.yml -f environment=staging

# Deploy to production (requires approval)
gh workflow run cd-deploy.yml -f environment=prod
```

### 2. Manual Deployment

#### Local Development Deployment:
```bash
# Clone repository
git clone https://github.com/Copubah/aws-slack-alerts-terraform.git
cd aws-slack-alerts-terraform

# Configure environment
cp environments/dev/terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# Setup backend
cat > backend.tf << EOF
terraform {
  backend "s3" {
    bucket = "your-terraform-state-dev"
    key    = "dev/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
    dynamodb_table = "terraform-lock-dev"
  }
}
EOF

# Deploy
terraform init
terraform plan
terraform apply
```

## Testing Deployment

### 1. Automated Testing
The CI/CD pipeline automatically tests deployments:
- Terraform validation
- Lambda function tests
- Infrastructure connectivity tests
- Slack notification tests

### 2. Manual Testing
```bash
# Test SNS topic
SNS_TOPIC_ARN=$(terraform output -raw sns_topic_arn)
aws sns publish \
  --topic-arn "$SNS_TOPIC_ARN" \
  --subject "Test Alert" \
  --message "This is a test message"

# Check Lambda logs
aws logs tail "/aws/lambda/aws-slack-alerts-slack-notifier" --follow

# Verify GuardDuty is enabled
aws guardduty list-detectors

# Check CloudWatch alarms
aws cloudwatch describe-alarms --alarm-names "aws-slack-alerts-high-cpu"
```

## Monitoring Deployments

### 1. GitHub Actions Monitoring
- Monitor workflow runs in the Actions tab
- Check deployment status and logs
- Review security scan results
- Monitor cost reports

### 2. AWS Monitoring
- CloudWatch dashboards for infrastructure metrics
- GuardDuty findings for security events
- Cost Explorer for spending analysis
- CloudTrail for API activity

### 3. Slack Monitoring
- Deployment notifications in Slack
- Alert testing confirmations
- Error notifications from failed deployments

## Rollback Procedures

### 1. Automated Rollback
```bash
# Rollback to previous version
git revert HEAD
git push origin main

# Or deploy specific version
gh workflow run cd-deploy.yml -f environment=prod
```

### 2. Manual Rollback
```bash
# Checkout previous version
git checkout <previous-commit-hash>

# Deploy previous version
terraform plan
terraform apply
```

### 3. Emergency Procedures
```bash
# Destroy infrastructure if needed
gh workflow run cd-deploy.yml -f environment=prod -f destroy=true

# Or manually
terraform destroy -auto-approve
```

## Troubleshooting

### Common Issues

1. **Terraform State Lock**:
   ```bash
   # Force unlock if needed (use carefully)
   terraform force-unlock <lock-id>
   ```

2. **Lambda Deployment Issues**:
   ```bash
   # Check Lambda function logs
   aws logs describe-log-groups --log-group-name-prefix "/aws/lambda"
   ```

3. **SNS Permission Issues**:
   ```bash
   # Verify SNS topic policy
   aws sns get-topic-attributes --topic-arn <topic-arn>
   ```

4. **GuardDuty Issues**:
   ```bash
   # Check GuardDuty status
   aws guardduty get-detector --detector-id <detector-id>
   ```

### Getting Help

1. Check GitHub Issues for known problems
2. Review CloudWatch logs for error details
3. Verify AWS permissions and quotas
4. Test Slack webhook URLs manually
5. Contact maintainers via GitHub Issues

## Security Considerations

### 1. Secrets Management
- Never commit secrets to Git
- Use GitHub encrypted secrets
- Rotate credentials regularly
- Use least privilege IAM policies

### 2. Infrastructure Security
- Enable GuardDuty in all environments
- Monitor CloudTrail logs
- Use encrypted S3 buckets for state
- Implement proper network security groups

### 3. Deployment Security
- Require reviews for production deployments
- Use branch protection rules
- Enable security scanning in CI/CD
- Monitor for infrastructure drift

## Cost Optimization

### 1. Environment-Specific Budgets
- Development: $50/month
- Staging: $150/month
- Production: $500/month

### 2. Cost Monitoring
- Weekly cost reports via GitHub Actions
- Budget alerts via AWS Budgets
- Unused resource detection
- Right-sizing recommendations

### 3. Optimization Strategies
- Use appropriate Lambda memory settings
- Optimize CloudWatch log retention
- Review GuardDuty data sources
- Monitor SNS message volumes