import boto3
import json

# Configure the EKS client for LocalStack
eks = boto3.client("eks", endpoint_url="http://localhost:4566", region_name="us-east-1")
iam = boto3.client("iam", endpoint_url="http://localhost:4566", region_name="us-east-1")

def solution():
    # 1. Create a mock \"Developer\" IAM Role
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    print("Creating IAM Role: K8sAdminRole...")
    role_response = iam.create_role(
        RoleName="K8sAdminRole",
        AssumeRolePolicyDocument=json.dumps(trust_policy)
    )
    dev_role_arn = role_response["Role"]["Arn"]
    print(f"Role Created: {dev_role_arn}")

    # 2. Create an Access Entry for the Developer Role
    print("Creating EKS Access Entry for PortfolioCluster...")
    eks.create_access_entry(
        clusterName="PortfolioCluster",
        principalArn=dev_role_arn,
        kubernetesGroups=["system:masters"]
    )
    print("Access Entry Created Successfully.")

if __name__ == "__main__":
    solution()
