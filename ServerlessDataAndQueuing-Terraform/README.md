AWS Cloud Automation & Serverless Data Queuing Stack
A production-grade Infrastructure as Code (IaC) configuration demonstrating automated serverless data pipelines, resilient queuing systems, incident tracking, and monitoring using Terraform.
This stack is designed for automated AWS resource orchestration and local development using MiniStack / LocalStack (`localhost:4566`).
🏗️ Architecture & Core Components
The configuration in `main.tf` provisions and connects the following core serverless and monitoring resources:
Amazon S3 (`sre-audit-logs-local`): Secure bucket configured for audit log retention and storage.
Amazon SQS (`sre-dlq`): Dead-Letter Queue designed for robust error handling and failed message isolation.
Amazon SNS (`sre-alerts-topic`): Notification topic coupled with SQS subscriptions for automated alerting workflows.
Amazon DynamoDB (`incidents-table`): On-demand (`PAY_PER_REQUEST`) NoSQL table for high-throughput incident tracking and state management.
Amazon CloudWatch (`high-error-rate-alarm`): Automated metric alarm monitoring target application `5XX` error counts with threshold triggers.
🚀 Getting Started & Local Testing
This configuration is fully compatible with local AWS emulators like MiniStack or LocalStack.
Prerequisites
Terraform (v1.0+)
Docker (running MiniStack/LocalStack on port `4566`)
1. Start Local Emulator
Ensure your local MiniStack container is active:
```bash
docker start ministack
```
2. Initialize Terraform
Initialize the Terraform providers:
```bash
terraform init
```
3. Review and Apply
Preview the execution plan:
```bash
terraform plan
```
Deploy the stack:
```bash
terraform apply -auto-approve
```
