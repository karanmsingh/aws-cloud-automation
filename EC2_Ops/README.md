# EC2 Tag-Based Automation & Local Testbed (`EC2_Ops`)

This directory houses the operational tooling and Infrastructure as Code (IaC) setup required to manage EC2 instance lifecycles dynamically using AWS tags. It includes a Python automation tool leveraging `boto3` and a modular Terraform testbed optimized for local simulation using LocalStack or MiniStack configurations.

## Directory Structure

*   `aws_ops_tool.py`: Production-ready Python CLI utility designed to scan, filter, and safely manage the runtime states of EC2 instances globally using targeted tag filters.
*   `ec2_instances.tf`: Declarative Terraform configuration provisioning a complete test environment, including a custom VPC, subnet architecture, security configurations, and dynamic tagged test instances.

---

## Features

*   **Dry-Run Architecture:** The lifecycle script implements a strict evaluation mechanism ensuring no cloud resources are altered without absolute verification.
*   **Decoupled Tag Filtering:** Operators can dynamically query infrastructures using standard environment, classification, or custom business logic keys.
*   **Local Simulation Bed:** Pre-configured Terraform blocks map safely to standard mock endpoints, preventing unwanted cloud spend during feature testing.

---

## Prerequisites

Ensure your local development environment has the required runtime configurations:

```bash
# Install specific cloud SDKs and tools
pip install boto3 argparse
```

Configure your environment context for local testing:
```bash
export AWS_ENDPOINT_URL="http://localhost:4566"
```

---

## Usage Guide

### 1. Provisioning the Local Infrastructure
Initialize the testbed architecture and apply your changes using the local pipeline configuration:

```bash
terraform init
terraform plan
terraform apply -auto-approve
```

### 2. Executing the Automation Tooling
Query the targeted infrastructure securely using dynamic CLI flags:

```bash
# Run a non-destructive dry-run discovery scan
python3 aws_ops_tool.py --tag-key Environment --tag-value Dev

# Execute active state modification sequences across matching targets
python3 aws_ops_tool.py --tag-key Environment --tag-value Dev --execute
```

---

## Engineering Guidelines

*   **Fail-Safe Design Principle:** Modifications to runtime states default to dry-run validation. The `--execute` parameters require deliberate operator injection.
*   **Strict Resource Hygiene:** Always tear down local test architecture once execution runs complete to free up system capacity:
    ```bash
    terraform destroy -auto-approve
    ```
