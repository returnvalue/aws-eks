# Lab 3: Serverless Data Plane (Fargate Profiles)

**Goal:** We want certain workloads to run entirely serverless. Create a Fargate Profile so that any pod deployed to the `serverless-apps` namespace is automatically scheduled on AWS Fargate instead of our EC2 nodes.

```bash
# 1. Create the Fargate Pod Execution Role
cat <<EOF > fargate-trust.json
{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "eks-fargate-pods.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}
EOF
FARGATE_ROLE_ARN=$(awslocal iam create-role --role-name EKSFargateRole --assume-role-policy-document file://fargate-trust.json --query 'Role.Arn' --output text)

# 2. Create the Fargate Profile targeting a specific Kubernetes namespace
awslocal eks create-fargate-profile \
  --cluster-name PortfolioCluster \
  --fargate-profile-name ServerlessProfile \
  --pod-execution-role-arn $FARGATE_ROLE_ARN \
  --subnets $SUBNET_1 $SUBNET_2 \
  --selectors namespace=serverless-apps
```

## 🧠 Key Concepts & Importance

- **AWS Fargate for EKS:** A serverless compute engine for containers. You no longer need to provision, configure, or scale groups of virtual machines to run Kubernetes pods.
- **Fargate Profile:** Defines which pods use Fargate when they are launched. You can define selectors that match namespaces and labels.
- **Pod Execution Role:** An IAM role that provides the Fargate infrastructure with permissions to pull images from ECR and send logs to CloudWatch on behalf of the pods.
- **Namespace-Based Selection:** A common strategy is to dedicate specific Kubernetes namespaces to Fargate, allowing for a mix of EC2 and Fargate workloads within the same cluster.
- **No Management Overhead:** Fargate eliminates the operational burden of managing worker nodes, including OS patching and capacity planning.

## 🛠️ Command Reference

- `eks create-fargate-profile`: Creates a Fargate profile for your Amazon EKS cluster.
    - `--cluster-name`: The name of the cluster.
    - `--fargate-profile-name`: A unique name for the profile.
    - `--pod-execution-role-arn`: The ARN of the IAM role that provides permissions for the Fargate pods.
    - `--subnets`: The subnets where the Fargate pods will be placed.
    - `--selectors`: The Kubernetes namespace and labels to use for selecting pods to run on Fargate.
