# Lab 7: Connecting to the Cluster (kubeconfig)

**Goal:** Generate the local configuration file required by `kubectl` to authenticate with the EKS API server and manage Kubernetes resources.

```bash
# Generate and update the local kubeconfig file
awslocal eks update-kubeconfig \
  --name PortfolioCluster \
  --region us-east-1
aws eks update-kubeconfig \
  --name PortfolioCluster \
  --region us-east-1
```

## 🧠 Key Concepts & Importance

- **kubeconfig:** A file used to configure access to Kubernetes clusters. It contains cluster details, certificates, and authentication tokens.
- **kubectl Integration:** `kubectl` uses the kubeconfig file to find the information it needs to choose a cluster and communicate with the API server of that cluster.
- **Contexts:** Kubeconfig files can contain multiple "contexts," allowing you to easily switch between different clusters (e.g., dev, staging, prod) or different users.
- **Authentication:** For EKS, the kubeconfig usually invokes the AWS CLI (or `awslocal`) to generate a temporary token for authentication, ensuring that Kubernetes access is tied to IAM permissions.
- **API Server Communication:** Once configured, you can use standard Kubernetes commands (e.g., `kubectl get pods`, `kubectl apply`) to manage your serverless or node-based workloads.

## 🛠️ Command Reference

- `eks update-kubeconfig`: Configures `kubectl` to communicate with your EKS cluster.
    - `--name`: The name of the EKS cluster.
    - `--region`: The AWS region where the cluster is located.

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
