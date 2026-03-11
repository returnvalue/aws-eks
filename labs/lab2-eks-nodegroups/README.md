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

# 2. Create the Managed Node Group
awslocal eks create-nodegroup \
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
