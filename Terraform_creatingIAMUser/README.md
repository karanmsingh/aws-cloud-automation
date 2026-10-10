# 🚀 AWS IAM Infrastructure Automation (Terraform)

A professional showcase of automated Identity and Access Management (IAM) provisioning using HashiCorp Terraform. This project demonstrates the ability to define, manage, and deploy cloud infrastructure through code (IaC).

## 🛠️ Tech Stack
* **Cloud Provider:** AWS (Amazon Web Services)
* **Infrastructure Tooling:** Terraform (HCL)
* **Primary Services:** IAM (Identity & Access Management)

## 📋 Architectural Overview
This configuration automates the full lifecycle of a privileged administrative user. By executing this code, Terraform ensures the following state in the AWS environment:

1.  **Identity Provisioning:** Creates a new IAM User entity named `lucy`.
2.  **Policy Definition:** Programmatically defines a Managed IAM Policy (`AdminUsers`) with full administrative scope.
3.  **Resource Mapping:** Performs a programmatic attachment to link the identity to the permissions.

## 🏗️ Technical Highlights

### 1. Provider Configuration
The code utilizes the official `hashicorp/aws` provider, configured for the `us-east-1` region. This demonstrates an understanding of regional scoping in AWS architecture.

### 2. Declarative Resource Management
* **User Creation:** Uses the `aws_iam_user` resource with metadata tagging for organizational tracking.
* **Heredoc Syntax:** Employs `EOF` (Heredoc) syntax within the `aws_iam_policy` resource to maintain clean, readable JSON policy documents directly within the HCL code.

### 3. Implicit & Explicit Dependency Mapping
The `aws_iam_user_policy_attachment` resource demonstrates advanced Terraform dependency management by referencing the user name and policy ARN directly from the other resources:

```hcl
user       = aws_iam_user.admin-user.name
policy_arn = aws_iam_policy.adminUser.arn
