# Lab 1: Network Foundation & Control Plane

**Goal:** EKS requires a VPC with at least two subnets in different Availability Zones. We will create the network, the EKS Service Role, and provision the managed Control Plane.
```bash
# 1. Create VPC and Subnets
VPC_ID=$(awslocal ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
SUBNET_1=$(awslocal ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --availability-zone us-east-1a --query 'Subnet.SubnetId' --output text)
SUBNET_1=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.1.0/24 --availability-zone us-east-1a --query 'Subnet.SubnetId' --output text)
SUBNET_2=$(awslocal ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.2.0/24 --availability-zone us-east-1b --query 'Subnet.SubnetId' --output text)
SUBNET_2=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block 10.0.2.0/24 --availability-zone us-east-1b --query 'Subnet.SubnetId' --output text)

# 2. Create the EKS Cluster Service Role
cat <<EOF > eks-trust.json
{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "eks.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}
EOF
CLUSTER_ROLE_ARN=$(awslocal iam create-role --role-name EKSClusterRole --assume-role-policy-document file://eks-trust.json --query 'Role.Arn' --output text)
CLUSTER_ROLE_ARN=$(aws iam create-role --role-name EKSClusterRole --assume-role-policy-document file://eks-trust.json --query 'Role.Arn' --output text)

# 3. Create the EKS Cluster (This provisions the managed Control Plane)
awslocal eks create-cluster \
  --name PortfolioCluster \
  --role-arn $CLUSTER_ROLE_ARN \
  --resources-vpc-config subnetIds=$SUBNET_1,$SUBNET_2
aws eks create-cluster \
  --name PortfolioCluster \
  --role-arn $CLUSTER_ROLE_ARN \
  --resources-vpc-config subnetIds=$SUBNET_1,$SUBNET_2
```

## 🧠 Key Concepts & Importance

- **EKS Control Plane:** The managed Kubernetes master node. AWS handles its availability, scalability, and security.
- **EKS Cluster Role:** An IAM role that provides the EKS control plane with permissions to make calls to other AWS services on your behalf.
- **Multi-AZ Requirement:** EKS requires subnets in at least two Availability Zones to ensure high availability for the Kubernetes API server and etcd.
- **Managed Service:** By using EKS, you avoid the complexity of manually installing, operating, and maintaining your own Kubernetes control plane.

## 🛠️ Command Reference

- `ec2 create-vpc`: Creates a VPC with the specified CIDR block.
- `ec2 create-subnet`: Creates a subnet in a specific Availability Zone.
- `iam create-role`: Creates an IAM role with a trust policy for the EKS service.
- `eks create-cluster`: Creates an Amazon EKS control plane.
    - `--name`: Unique name for the cluster.
    - `--role-arn`: The ARN of the IAM role that provides permissions for the EKS control plane.
    - `--resources-vpc-config`: Specifies the subnets where EKS will place the ENIs for the control plane.

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
