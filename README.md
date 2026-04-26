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
* **EKS Security:** Implementing IRSA (IAM Roles for Service Accounts) and modern Access Entries.
* **Cluster Add-ons:** Managing operational software like VPC CNI natively via the EKS API.
* **Cluster Connectivity:** Configuring `kubectl` to manage resources via `update-kubeconfig`.
* **Kubernetes Orchestration:** (Upcoming) Deploying applications using Helm and kubectl.
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
> **Session Persistence:** These labs rely on bash variables (like `$VPC_ID`, `$CLUSTER_ROLE_ARN`, `$OIDC_URL`, etc.). Run all commands in the same terminal session to maintain context.

## 📚 Labs Index
1. [Lab 1: Network Foundation & Control Plane](./labs/lab1-eks-foundation/README.md)
2. [Lab 2: Data Plane (Managed Node Groups)](./labs/lab2-eks-nodegroups/README.md)
3. [Lab 3: Serverless Data Plane (Fargate Profiles)](./labs/lab3-eks-fargate-profiles/README.md)
4. [Lab 4: Security Identity (OIDC & IRSA)](./labs/lab4-eks-irsa/README.md)
5. [Lab 5: Cluster Add-ons Management (VPC CNI)](./labs/lab5-eks-addons/README.md)
6. [Lab 6: Modern Access Management (Access Entries)](./labs/lab6-eks-access-management/README.md)
7. [Lab 7: Connecting to the Cluster (kubeconfig)](./labs/lab7-eks-kubeconfig/README.md)

---

💡 **Pro Tip: Using `aws` instead of `awslocal`**

If you prefer using the standard `aws` CLI without the `awslocal` wrapper or repeating the `--endpoint-url` flag, you can configure a dedicated profile in your AWS config files.

### 1. Configure your Profile
Add the following to your `~/.aws/config` file:
```ini
[profile localstack]
region = us-east-1
output = json
# This line redirects all commands for this profile to LocalStack
endpoint_url = http://localhost:4566
```

Add matching dummy credentials to your `~/.aws/credentials` file:
```ini
[localstack]
aws_access_key_id = test
aws_secret_access_key = test
```

### 2. Use it in your Terminal
You can now run commands in two ways:

**Option A: Pass the profile flag**
```bash
aws iam create-user --user-name DevUser --profile localstack
```

**Option B: Set an environment variable (Recommended)**
Set your profile once in your session, and all subsequent `aws` commands will automatically target LocalStack:
```bash
export AWS_PROFILE=localstack
aws iam create-user --user-name DevUser
```

### Why this works
- **Precedence**: The AWS CLI (v2) supports a global `endpoint_url` setting within a profile. When this is set, the CLI automatically redirects all API calls for that profile to your local container instead of the real AWS cloud.
- **Convenience**: This allows you to use the standard documentation commands exactly as written, which is helpful if you are copy-pasting examples from AWS labs or tutorials.
