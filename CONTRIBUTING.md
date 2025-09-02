# Contributing to AWS Slack Alerts

Thank you for your interest in contributing to this project!

## Development Setup

1. **Prerequisites**
   - Terraform >= 1.0
   - Python 3.8+
   - AWS CLI configured
   - Git

2. **Local Development**
   ```bash
   git clone https://github.com/Copubah/aws-slack-alerts-terraform.git
   cd aws-slack-alerts-terraform
   
   # Install Python dependencies for diagram generation
   pip install -r requirements.txt
   
   # Copy and configure variables
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your values
   ```

3. **Testing Changes**
   ```bash
   # Validate Terraform configuration
   terraform init
   terraform validate
   terraform plan
   
   # Generate architecture diagram
   python architecture.py
   ```

## Contribution Guidelines

### Code Style
- Follow Terraform best practices
- Use consistent naming conventions
- Add comments for complex logic
- Keep resources organized in logical files

### Commit Messages
Use conventional commit format:
- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `refactor:` code refactoring
- `test:` adding tests

### Pull Request Process
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test thoroughly
5. Update documentation if needed
6. Submit a pull request

### Testing
- Test all Terraform configurations
- Verify Lambda function works with sample events
- Ensure Slack notifications are properly formatted
- Test with different AWS services

## Project Structure

```
├── provider.tf          # AWS provider configuration
├── variables.tf         # Input variables
├── sns.tf              # SNS topic and policies
├── lambda.tf           # Lambda function and IAM
├── lambda_function.py  # Python Lambda code
├── cloudwatch.tf       # CloudWatch alarms
├── guardduty.tf        # GuardDuty configuration
├── events.tf           # EventBridge rules
├── budgets.tf          # AWS Budget alerts
├── outputs.tf          # Output values
├── architecture.py     # Diagram generation
└── README.md           # Documentation
```

## Security Considerations

- Never commit sensitive data (API keys, webhooks)
- Use Terraform variables for sensitive values
- Follow AWS IAM least privilege principle
- Validate all user inputs

## Questions?

Feel free to open an issue for questions or suggestions!