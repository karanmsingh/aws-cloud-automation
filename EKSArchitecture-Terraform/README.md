# Production-Grade Amazon EKS Architecture & Hybrid Infrastructure Automation

An enterprise-grade Infrastructure as Code (IaC) project demonstrating the automated provisioning of a secure, production-ready **Amazon Elastic Kubernetes Service (EKS)** environment using **Terraform**, paired with a robust local hybrid execution model (**Kind**) for container workload orchestration and validation.

---

## 🏗️ Architectural Overview

This project implements a scalable, secure, and highly available cloud-native network and compute topology designed in accordance with **AWS Well-Architected Framework** principles:

* **Networking Layer:** Custom Virtual Private Cloud (VPC) (`10.0.0.0/16`) spanning multiple Availability Zones (`us-east-1a`, `us-east-1b`) equipped with public subnets, an Internet Gateway (IGW), and custom route table associations to manage external traffic flow.
* **Security & Identity (IAM):** Dedicated AWS IAM roles and strict least-privilege policy attachments enforcing security boundaries across the control plane (`AmazonEKSClusterPolicy`) and managed worker nodes (`AmazonEKSWorkerNodePolicy`, `AmazonEKS_CNI_Policy`, `AmazonEC2ContainerRegistryReadOnly`).
* **Control Plane & Compute:** Provisioned a managed EKS v1.30 Control Plane (`production-cluster`) coupled with an auto-scaling managed worker node group (`production-worker-group`).
* **Container Workload Layer:** Deployed a high-availability microservice architecture featuring redundant **Nginx** replicas with explicit CPU/memory resource limits, exposed externally via a Kubernetes `NodePort` service (`30080`).

---

## 🧠 Engineering Design: The Hybrid Local Workflow

In professional cloud engineering, testing complex container runtimes locally without incurring heavy cloud provider expenses requires creative architecture. This project bridges **Cloud Management Plane Emulation** with a **Local Kubernetes Runtime**:

1. **Infrastructure Provisioning (Terraform & MiniStack):** 
   * Declaratively automates the creation of all core AWS cloud resources. The local simulation layer intercepts AWS management APIs (`CreateCluster`, `CreateNodeGroup`, `CreateVpc`), allowing complete 100% IaC validation.
2. **Workload Runtime (Kind - Kubernetes in Docker):** 
   * Integrates a lightweight, containerized Kubernetes runtime to execute the `kube-apiserver`, scheduler, and worker node daemons. This allows native `kubectl` operations, pod scheduling, and end-to-end traffic routing validation.

---

## 🚀 Deployment & Reproduction Guide

### Prerequisites
* Terraform (`>= 1.5.0`)
* Docker & MiniStack (running locally on port `4566`)
* `kubectl` & `kind` (Kubernetes in Docker)

---

### Step 1: Provision Cloud Infrastructure with Terraform
Initialize and apply the Terraform configuration to build the VPC, IAM security roles, EKS control plane, and managed worker node group:

```bash
terraform init
terraform apply -auto-approve
```

---

### Step 2: Spin Up the Local Kubernetes Runtime (Kind)
Provision the local Kind cluster with explicit port mapping to route external traffic to your container workloads:

```bash
# Create local Kind configuration
cat <<EOF > kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30080
    hostPort: 8080
    protocol: TCP
EOF

# Create the cluster
kind create cluster --name production-workloads --config kind-config.yaml
```

---

### Step 3: Deploy and Verify Workloads
Apply the containerized Nginx application manifest to your cluster:

```bash
kubectl apply -f nginx-app.yaml
```

Verify that pods are running successfully and test external access:
```bash
# Check pod replication and status across nodes
kubectl get pods -l app=nginx -o wide

# Test the active service endpoint
curl http://localhost:8080
```

---

## 🛠️ Key Technical Competencies Demonstrated
* **Infrastructure as Code (IaC):** Advanced Terraform syntax, provider configuration, dependency mapping (`depends_on`), and resource state management.
* **Cloud Networking & Security:** Custom VPC subnetting, Internet Gateway routing, and fine-grained IAM policy assignment for containerized environments.
* **Container Orchestration:** Kubernetes `Deployments`, `NodePort` services, replica management, and container resource constraint tuning.
* **DevOps Problem-Solving:** Designing effective local hybrid testing environments to bridge cloud provider APIs with native container runtimes.
