# Production-Grade Amazon EKS Architecture & Infrastructure Automation

An Infrastructure as Code (IaC) project designed to provision, validate, and document a production-ready **Amazon Elastic Kubernetes Service (EKS)** cluster infrastructure using **Terraform** and local cloud simulation tools (**MiniStack**).

---

## 🏗️ Architecture Overview

This project implements a secure, highly available cloud-native network and compute layout adhering to AWS well-architected framework principles:

* **Networking Layer:** Custom Virtual Private Cloud (VPC) (`10.0.0.0/16`) spanning multiple Availability Zones (`us-east-1a`, `us-east-1b`) with public subnets, an Internet Gateway (IGW), and custom route table associations.
* **Security & Identity (IAM):** Dedicated IAM roles and policy attachments for both the control plane (`AmazonEKSClusterPolicy`) and managed worker nodes (`AmazonEKSWorkerNodePolicy`, `AmazonEKS_CNI_Policy`, `AmazonEC2ContainerRegistryReadOnly`).
* **Control Plane:** Managed EKS v1.30 Control Plane (`production-cluster`).
* **Compute Layer:** Managed EKS Worker Node Group (`production-worker-group`) configured with auto-scaling parameters.

---

## 🚀 Deployment Walkthrough

### Prerequisites
* Terraform (>= 1.5.0)
* Docker & MiniStack running locally on port `4566`
* AWS CLI configured with mock credentials

### Step 1: Initialize Terraform
Initialize the provider plugins and backend workspace:
```bash
terraform init
