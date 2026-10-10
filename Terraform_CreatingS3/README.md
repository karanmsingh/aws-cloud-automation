# 🪣 AWS S3 Infrastructure Automation (Terraform)

This project demonstrates the use of Infrastructure as Code (IaC) to programmatically provision and manage cloud storage resources on Amazon Web Services (AWS) using HashiCorp Terraform.

## 📋 What this Terraform configuration does:

The `main.tf` file automates the following infrastructure tasks:

1.  **Provider Initialization**: Configures the official AWS provider to communicate with your account and targets the `us-east-1` (N. Virginia) region for deployment.
2.  **S3 Bucket Provisioning**: Creates a high-availability Simple Storage Service (S3) bucket named `kaststb-terraform`.
3.  **Global Namespace Compliance**: Adheres to AWS S3 naming requirements by utilizing a unique, DNS-compliant, all-lowercase naming convention.
4.  **Resource Tagging**: Automatically applies metadata tags to the bucket (e.g., `Description = "Created with Terraform."`) to ensure better resource organization and cost-tracking within the AWS Console.

## 🏗️ Technical Highlights

*   **Declarative Syntax**: Uses HCL (HashiCorp Configuration Language) to define the desired end-state of the cloud environment.
*   **Automated Lifecycle**: Enables a predictable "Init -> Plan -> Apply" workflow, ensuring that the infrastructure is reproducible and version-controlled.
*   **State Management**: By using Terraform, the lifecycle of this bucket is managed via a state file, allowing for easy updates or clean destruction of resources in the future.

## 🚀 Deployment Workflow

```bash
# Prepare the directory for Terraform
terraform init

# Preview the infrastructure changes
terraform plan

# Deploy the S3 bucket to the AWS Cloud
terraform apply -auto-approve
