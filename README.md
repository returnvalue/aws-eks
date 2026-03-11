# AWS Elastic Kubernetes Service (EKS) Labs (LocalStack Pro)

![AWS](https://img.shields.io/badge/AWS-EKS_Kubernetes-FF9900?style=for-the-badge&logo=amazonaws)
![LocalStack](https://img.shields.io/badge/LocalStack-Pro-000000?style=for-the-badge)

This repository contains hands-on labs demonstrating core Amazon EKS concepts, from foundational cluster provisioning and networking to node group management, deployments, and security. Using [LocalStack Pro](https://localstack.cloud/), we simulate a complete AWS Kubernetes environment locally.

## 🎯 Architecture Goals & Use Cases Covered
Based on AWS best practices (SAA-C03), these labs cover:
* **Control Plane Management:** Provisioning managed EKS clusters with IAM service roles.
* **Networking Foundation:** Designing multi-AZ VPCs required for Kubernetes reliability.
* **Worker Nodes:** Deploying and scaling EC2 Managed Node Groups.
* **Serverless Kubernetes:** Using Fargate Profiles to run pods without managing nodes.
* **Kubernetes Orchestration:** (Upcoming) Deploying applications using Helm and kubectl.
* **EKS Security:** (Upcoming) Implementing IRSA (IAM Roles for Service Accounts).
* **Observability:** (Upcoming) Monitoring clusters with CloudWatch container insights.

## ⚙️ Prerequisites

* [Docker](https://docs.docker.com/get-docker/) & Docker Compose
* [LocalStack Pro](https://app.localstack.cloud/) account and Auth Token
* [`awslocal` CLI](https://github.com/localstack/awscli-local) (a wrapper around the AWS CLI for LocalStack)
* [`kubectl`](https://kubernetes.io/docs/tasks/tools/) (optional, for interacting with the cluster)

## 🚀 Environment Setup

1. Configure your LocalStack Auth Token in `.env`:
   ```bash
   echo "YOUR_TOKEN=your_auth_token_here" > .env
   ```

2. Start LocalStack Pro:
   ```bash
   docker-compose up -d
   ```

> [!IMPORTANT]
> **Cumulative Architecture:** These labs are designed as a cumulative scenario. You are building an evolving Kubernetes infrastructure.
>
> **Session Persistence:** These labs rely on bash variables (like `$VPC_ID`, `$CLUSTER_ROLE_ARN`, `$FARGATE_ROLE_ARN`, etc.). Run all commands in the same terminal session to maintain context.

## 📚 Labs Index
1. [Lab 1: Network Foundation & Control Plane](./labs/lab1-eks-foundation/README.md)
2. [Lab 2: Data Plane (Managed Node Groups)](./labs/lab2-eks-nodegroups/README.md)
3. [Lab 3: Serverless Data Plane (Fargate Profiles)](./labs/lab3-eks-fargate-profiles/README.md)
