# Lab 6: Modern Access Management (Access Entries)

**Goal:** Instead of manually editing the risky `aws-auth` Kubernetes ConfigMap, use the modern AWS API to grant an external IAM Role administrative access to the cluster.

```bash
# 1. Create a mock "Developer" IAM Role
DEV_ROLE_ARN=$(awslocal iam create-role --role-name K8sAdminRole --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":"*"},"Action":"sts:AssumeRole"}]}' --query 'Role.Arn' --output text)

# 2. Create an Access Entry for the Developer Role
awslocal eks create-access-entry \
  --cluster-name PortfolioCluster \
  --principal-arn $DEV_ROLE_ARN \
  --kubernetes-groups system:masters
```

## 🧠 Key Concepts & Importance

- **EKS Access Entries:** A modern, AWS-native way to manage Kubernetes cluster access. It replaces the legacy `aws-auth` ConfigMap approach.
- **IAM Integration:** Seamlessly maps IAM principals (users or roles) to Kubernetes groups without needing to interact with the Kubernetes API directly.
- **Cluster Security:** Reduces the risk of lockouts or misconfigurations that often occurred when manually editing the `aws-auth` ConfigMap.
- **Auditability:** Access entries are AWS resources, making them easier to audit and manage via CloudTrail and IAM policies.
- **system:masters:** A built-in Kubernetes group that grants full administrative access to the cluster.

## 🛠️ Command Reference

- `iam create-role`: Creates a new IAM role.
- `eks create-access-entry`: Creates an access entry for a principal to access the EKS cluster.
    - `--cluster-name`: The name of the cluster.
    - `--principal-arn`: The ARN of the IAM principal (user or role).
    - `--kubernetes-groups`: The Kubernetes groups to which the principal is mapped.
