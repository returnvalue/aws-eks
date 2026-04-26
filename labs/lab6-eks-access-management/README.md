# Lab 6: Modern Access Management (Access Entries)

**Goal:** Instead of manually editing the risky `aws-auth` Kubernetes ConfigMap, use the modern AWS API to grant an external IAM Role administrative access to the cluster.
```bash
# 1. Create a mock "Developer" IAM Role
DEV_ROLE_ARN=$(awslocal iam create-role --role-name K8sAdminRole --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":"*"},"Action":"sts:AssumeRole"}]}' --query 'Role.Arn' --output text)
DEV_ROLE_ARN=$(aws iam create-role --role-name K8sAdminRole --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":"*"},"Action":"sts:AssumeRole"}]}' --query 'Role.Arn' --output text)

# 2. Create an Access Entry for the Developer Role
awslocal eks create-access-entry \
  --cluster-name PortfolioCluster \
  --principal-arn $DEV_ROLE_ARN \
  --kubernetes-groups system:masters
aws eks create-access-entry \
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
