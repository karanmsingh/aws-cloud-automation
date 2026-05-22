\# Automated Production-Ready Amazon EKS Cluster Architecture



This repository documents the structural engineering, configuration, and successful deployment of a highly available, enterprise-grade Amazon Elastic Kubernetes Service (EKS) cluster architecture using `eksctl` and `kubectl`.



\## Technical Architecture Overview



The infrastructure decouples the Kubernetes control plane from worker node groups, utilizing a highly available network topology distributed across multiple Availability Zones (AZs) within a dedicated AWS Virtual Private Cloud (VPC).



```text

&#x20;                     +---------------------------------------+

&#x20;                     |       AWS Region: us-east-2           |

&#x20;                     |            (Ohio)                     |

&#x20;                     +---------------------------------------+

&#x20;                                         |

&#x20;                                         v

&#x20;                     +---------------------------------------+

&#x20;                     |        Dedicated VPC Network          |

&#x20;                     +---------------------------------------+

&#x20;                                         |

&#x20;                 +-----------------------+-----------------------+

&#x20;                 |                                               |

&#x20;                 v                                               v

&#x20;    +-------------------------+                     +-------------------------+

&#x20;    |   Availability Zone A   |                     |   Availability Zone B   |

&#x20;    |      (us-east-2a)       |                     |      (us-east-2b)       |

&#x20;    +-------------------------+                     +-------------------------+

&#x20;    | \[Public Subnet]         |                     | \[Public Subnet]         |

&#x20;    |  192.168.0.0/19         |                     |  192.168.32.0/19        |

&#x20;    |                         |                     |                         |

&#x20;    |  -> Worker Node 1       |                     |  -> Worker Node 2       |

&#x20;    |     (t3.medium)         |                     |     (t3.medium)         |

&#x20;    |                         |                     |                         |

&#x20;    | \[Private Subnet]        |                     | \[Private Subnet]        |

&#x20;    |  192.168.64.0/19        |                     |  192.168.96.0/19        |

&#x20;    +-------------------------+                     +-------------------------+

&#x20;                 |                                               |

&#x20;                 +-----------------------+-----------------------+

&#x20;                                         |

&#x20;                                         v

&#x20;                     +---------------------------------------+

&#x20;                     |         AWS Managed EKS Add-ons       |

&#x20;                     |  (vpc-cni, kube-proxy, coredns, etc.) |

&#x20;                     +---------------------------------------+





Core Specifications \& Features

Cluster Management: Orchestrated natively via eksctl using AWS CloudFormation automated stacks.



Kubernetes Control Plane: Version 1.34 running a fully-managed, highly available control plane.



Worker Nodes: Managed Node Group (eksdemo2-ng-public1) dynamically scaling between 2 to 4 t3.medium instances executing the modern Amazon Linux 2023 optimized AMI.



Network Isolation: Structured CIDR allocation across Public and Private subnets per AZ to enforce secure ingress routing policies.



IAM Core Extensions: Embedded flags enabling direct integration hooks for Auto Scaling Groups (ASG), ExternalDNS, Amazon Elastic Container Registry (ECR), AWS App Mesh, and AWS Application Load Balancer (ALB) Ingress Controllers.



Deployment \& Configuration History

1\. Infrastructure Bottlenecks \& Troubleshooting Logs

The architecture iteratively moved through three distinct operational adjustments based on infrastructure limits encountered during initial runs in us-east-1:



KMS Encryption State Lock: Custom storage volume flag overrides triggered an AWS Key Management Service error (Client.InvalidKMSKey.InvalidState). The storage profile was streamlined to fallback cleanly onto default production-ready EBS volumes.



VPC Hard Limits: Reaching the region's maximum network allowance quota (5 VPC limit) caused an immediate CloudFormation deployment rollback (ROLLBACK\_IN\_PROGRESS).



The Resolution: Executed a clean regional pivot to us-east-2 (Ohio), providing a completely pristine virtual networking footprint and a zeroed resource quota canvas.



2\. Final Unified Initialization Command

The complete cluster infrastructure, control plane, required networking paths, and worker node node-groups were provisioned concurrently using the following streamlined command execution:



PowerShell





eksctl create cluster --name=eksdemo2 \\

&#x20;                     --region=us-east-2 \\

&#x20;                     --zones=us-east-2a,us-east-2b \\

&#x20;                     --nodegroup-name=eksdemo2-ng-public1 \\

&#x20;                     --node-type=t3.medium \\

&#x20;                     --nodes=2 \\

&#x20;                     --nodes-min=2 \\

&#x20;                     --nodes-max=4 \\

&#x20;                     --asg-access \\

&#x20;                     --external-dns-access \\

&#x20;                     --full-ecr-access \\

&#x20;                     --appmesh-access \\

&#x20;                     --alb-ingress-access

Verification \& Operational Status

Upon stack stabilization, AWS CloudFormation automatically created the local secure Kubernetes configuration profile at \~/.kube/config. Verification commands confirm that the compute nodes have securely boot-strapped, fetched dependencies, and registered successfully into the cluster matrix.



PowerShell





\# Querying node infrastructure status via kubectl

kubectl get nodes -o wide

Output Logs

Plaintext





NAME                                             STATUS   ROLES    AGE   VERSION   INTERNAL-IP     OS-IMAGE               KERNEL-VERSION

ip-192-168-27-15.us-east-2.compute.internal      Ready    <none>   3m    v1.34.0   192.168.27.15   Amazon Linux 2023.6    6.1.102-113.122

ip-192-168-39-195.us-east-2.compute.internal     Ready    <none>   3m    v1.34.0   192.168.39.195  Amazon Linux 2023.6    6.1.102-113.122

Active Managed Add-ons

The deployment successfully initialized standard cluster systems engines as native EKS-managed add-ons:



vpc-cni: High-performance Amazon VPC container network interface.



kube-proxy: Local network service reflecting Kubernetes networking services on each node.



coredns: Flexible, extensible DNS server for cluster service discovery.



metrics-server: Resource metrics aggregator for horizontal pod autoscaling.



Future Architecture Extensions

When application workloads require programmatic access to managed external AWS components, the OpenID Connect (OIDC) service registry identity provider should be attached with the following terminal execution:



PowerShell





eksctl utils associate-iam-oidc-provider --region=us-east-2 --cluster=eksdemo2 --approve



\*\*\*

