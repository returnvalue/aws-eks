# Lab 5: Cluster Add-ons Management (VPC CNI)

**Goal:** EKS clusters rely on operational software (Add-ons) like the VPC CNI (for networking) and CoreDNS. Manage these natively through the AWS API to ensure they are updated and patched alongside the cluster control plane.

```bash
# Install the Amazon VPC CNI add-on directly via the EKS API
awslocal eks create-addon \
  --cluster-name PortfolioCluster \
  --addon-name vpc-cni \
  --addon-version v1.18.0-eksbuild.1
aws eks create-addon \
  --cluster-name PortfolioCluster \
  --addon-name vpc-cni \
  --addon-version v1.18.0-eksbuild.1
```

## 🧠 Key Concepts & Importance

- **EKS Add-ons:** Curated operational software that provides supporting capabilities to Kubernetes clusters. They are managed directly by AWS, simplifying the cluster lifecycle.
- **Amazon VPC CNI:** A Kubernetes Container Network Interface (CNI) plugin that provides native VPC networking for your pods. It allows pods to have the same IP address inside the pod as they do on the VPC network.
- **Managed Lifecycle:** By using the EKS Add-on API, AWS handles the installation, updates, and health monitoring of these critical components.
- **Version Compatibility:** EKS ensures that the add-on versions are compatible with your specific Kubernetes version, reducing the risk of broken clusters during upgrades.
- **Standardization:** Add-ons provide a standardized way to deploy core cluster services like CoreDNS, kube-proxy, and the VPC CNI.

## 🛠️ Command Reference

- `eks create-addon`: Installs an Amazon EKS add-on.
    - `--cluster-name`: The name of the cluster.
    - `--addon-name`: The name of the add-on (e.g., `vpc-cni`).
    - `--addon-version`: The specific version of the add-on to install.

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
