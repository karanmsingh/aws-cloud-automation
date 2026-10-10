# EC2 Tag-Based Automation & Local Testbed

Operational tooling and IaC setup for managing EC2 instance lifecycles based on tags.

## Files
- `aws_ops_tool.py`: Python CLI tool (`boto3`) to stop EC2 instances by tag key/value pairs with dry-run protection and JSON logging.
- `ec2_instances.tf`: Terraform configuration to provision test VPC and EC2 instances against MiniStack/LocalStack.

## Usage

```bash
# Set local MiniStack endpoints
export AWS_ENDPOINT_URL="http://localhost:4566"

# Run Dry-Run
python3 aws_ops_tool.py --tag-key Environment --tag-value Dev

# Run Active Execution
python3 aws_ops_tool.py --tag-key Environment --tag-value Dev --execute
