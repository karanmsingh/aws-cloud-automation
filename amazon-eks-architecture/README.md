# Automated Production-Ready Amazon EKS Cluster Architecture

This repository documents the structural engineering, configuration, and successful deployment of a highly available, enterprise-grade Amazon Elastic Kubernetes Service (EKS) cluster architecture using `eksctl` and `kubectl`.

## Technical Architecture Overview

The infrastructure decouples the Kubernetes control plane from worker node groups, utilizing a highly available network topology distributed across multiple Availability Zones (AZs) within a dedicated AWS Virtual Private Cloud (VPC).

```text
                      +---------------------------------------+
                      |       AWS Region: us-east-2           |
                      |            (Ohio)                     |
                      +---------------------------------------+
                                          |
                                          v
                      +---------------------------------------+
                      |        Dedicated VPC Network          |
                      +---------------------------------------+
                                          |
                  +-----------------------+-----------------------+
                  |                                               |
                  v                                               v
     +-------------------------+                     +-------------------------+
     |   Availability Zone A   |                     |   Availability Zone B   |
     |      (us-east-2a)       |                     |      (us-east-2b)       |
     +-------------------------+                     +-------------------------+
     | [Public Subnet]         |                     | [Public Subnet]         |
     |  192.168.0.0/19         |                     |  192.168.32.0/19        |
     |                         |                     |                         |
     |  -> Worker Node 1       |                     |  -> Worker Node 2       |
     |     (t3.medium)         |                     |     (t3.medium)         |
     |                         |                     |                         |
     | [Private Subnet]        |                     | [Private Subnet]        |
     |  192.168.64.0/19        |                     |  192.168.96.0/19        |
     +-------------------------+                     +-------------------------+
                  |                                               |
                  +-----------------------+-----------------------+
                                          |
                                          v
                      +---------------------------------------+
                      |         AWS Managed EKS Add-ons       |
                      |  (vpc-cni, kube-proxy, coredns, etc.) |
                      +---------------------------------------+
