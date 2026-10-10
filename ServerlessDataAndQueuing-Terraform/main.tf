AWS Cloud Automation & Serverless Data Queuing Stack
A production-grade, modular Infrastructure as Code (IaC) repository demonstrating automated serverless data pipelines, resilient queuing systems, incident tracking, and monitoring using Terraform.
This project is structured for both native AWS deployments and rapid local development and testing using MiniStack / LocalStack (`localhost:4566`).
---
🏗️ Architecture & Core Components
The core stack (`main.tf`) orchestrates a resilient serverless monitoring and event-driven data pipeline:
Amazon S3 (`sre-audit-logs-local`): Secure bucket configured for audit log retention and storage.
Amazon SQS (`sre-dlq`): Dead-Letter Queue designed for robust error handling and failed message isolation.
Amazon SNS (`sre-alerts-topic`): Notification topic coupled with SQS subscriptions for automated alerting workflows.
Amazon DynamoDB (`incidents-table`): On-demand (`PAY_PER_REQUEST`) NoSQL table for high-throughput incident tracking and state management.
Amazon CloudWatch (`high-error-rate-alarm`): Automated metric alarm monitoring target application `5XX` error counts with threshold triggers.
---
📂 Repository Structure
```text
aws-cloud-automation/
├── main.tf                    # Core infrastructure stack (S3, SQS, SNS, DynamoDB, CloudWatch)
├── ec2_instances.tf           # EC2 compute configurations
├── aws_ops_tool.py            # Python automation utility for AWS operations
├── efs_cleanup.py             # Automated maintenance script for EFS storage
├── URLEncoding.py             # Utility helper script for data formatting
├── Terraform_CreatingS3/      # Dedicated modular S3 provisioning setup
├── Terraform_creatingIAMUser/ # IAM user, group, and policy management
├── amazon-eks-architecture/   # EKS cluster reference architecture & notes
└── aws_ec2_ops/               # EC2 operational tooling and scripts
```
---
🚀 Getting Started & Local Testing
This project is fully compatible with local AWS emulators like MiniStack or LocalStack.
Prerequisites
Terraform (v1.0+)
Docker (running MiniStack/LocalStack on port `4566`)
1. Start Local Emulator
Ensure your local MiniStack container is active:
```bash
docker start ministack
```
2. Initialize Terraform
Navigate to the root directory and initialize the providers:
```bash
terraform init
```
3. Review and Apply
Preview the infrastructure execution plan:
```bash
terraform plan
```
Deploy the stack:
```bash
terraform apply -auto-approve
```
---
🛠️ Operational Tooling
In addition to Terraform configurations, this repository includes Python automation scripts (`aws_ops_tool.py`, `efs_cleanup.py`) designed to assist SREs with day-2 operational tasks, file cleanups, and data encoding utilities.
---
