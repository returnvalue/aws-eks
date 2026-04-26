# Lab 2: Data Plane (Managed Node Groups)

**Goal:** The control plane is running, but we have no worker nodes to schedule pods on. We will create an EC2 Managed Node Group to provide the underlying compute power for our Kubernetes cluster.
```bash
# 1. Create the Node IAM Role (Allows EC2 nodes to pull images and join the cluster)
cat <<EOF > node-trust.json
{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "ec2.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}
EOF
NODE_ROLE_ARN=$(awslocal iam create-role --role-name EKSNodeRole --assume-role-policy-document file://node-trust.json --query 'Role.Arn' --output text)
NODE_ROLE_ARN=$(aws iam create-role --role-name EKSNodeRole --assume-role-policy-document file://node-trust.json --query 'Role.Arn' --output text)

# 2. Create the Managed Node Group
awslocal eks create-nodegroup \
  --cluster-name PortfolioCluster \
  --nodegroup-name StandardCompute \
  --node-role $NODE_ROLE_ARN \
  --subnets $SUBNET_1 $SUBNET_2 \
  --instance-types t3.medium \
  --scaling-config minSize=1,maxSize=3,desiredSize=2
aws eks create-nodegroup \
  --cluster-name PortfolioCluster \
  --nodegroup-name StandardCompute \
  --node-role $NODE_ROLE_ARN \
  --subnets $SUBNET_1 $SUBNET_2 \
  --instance-types t3.medium \
  --scaling-config minSize=1,maxSize=3,desiredSize=2
```

## 🧠 Key Concepts & Importance

- **Data Plane:** The set of worker nodes that run your containerized applications. In EKS, these are typically EC2 instances.
- **Managed Node Groups:** AWS automates the provisioning and lifecycle management of the nodes. This includes updates, patches, and automatic scaling.
- **Node IAM Role:** Required for worker nodes to connect to the EKS control plane, pull images from ECR, and send logs to CloudWatch.
- **Auto Scaling:** The `scaling-config` defines the boundaries for how many nodes can be running, allowing the cluster to expand or contract based on workload demand.
- **Compute Diversity:** You can specify multiple instance types or use Spot instances within a node group to optimize for cost and performance.

## 🛠️ Command Reference

- `iam create-role`: Creates the IAM role that EC2 instances in the node group will assume.
- `eks create-nodegroup`: Provisions a managed group of EC2 instances for the cluster.
    - `--cluster-name`: The name of the cluster to add the node group to.
    - `--nodegroup-name`: A unique name for the node group.
    - `--node-role`: The ARN of the IAM role for the nodes.
    - `--subnets`: The subnets where the nodes will be placed (should match the cluster's subnets).
    - `--instance-types`: The EC2 instance type to use (e.g., `t3.medium`).
    - `--scaling-config`: Defines the minimum, maximum, and desired number of nodes.

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
