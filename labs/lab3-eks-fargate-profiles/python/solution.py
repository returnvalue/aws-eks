import boto3
import json

# Configure boto3 with localstack endpoint and us-east-1 region
def get_boto3_client(service_name):
    return boto3.client(
        service_name,
        endpoint_url="http://localhost:4566",
        region_name="us-east-1"
    )

eks = get_boto3_client('eks')
iam = get_boto3_client('iam')

def create_fargate_profile():
    # 1. Create the Fargate Pod Execution Role
    print("Creating IAM Role for EKS Fargate...")
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": {"Service": "eks-fargate-pods.amazonaws.com"}, "Action": "sts:AssumeRole"}]
    }
    
    role_response = iam.create_role(
        RoleName='EKSFargateRole',
        AssumeRolePolicyDocument=json.dumps(trust_policy)
    )
    fargate_role_arn = role_response['Role']['Arn']
    print(f"Created IAM Role: {fargate_role_arn}")

    # Fetch subnet IDs from the existing cluster
    print("Fetching cluster details to get subnets...")
    cluster_info = eks.describe_cluster(name='PortfolioCluster')
    subnet_ids = cluster_info['cluster']['resourcesVpcConfig']['subnetIds']
    print(f"Found subnets: {subnet_ids}")

    # 2. Create the Fargate Profile
    print("Creating EKS Fargate Profile...")
    eks.create_fargate_profile(
        clusterName='PortfolioCluster',
        fargateProfileName='ServerlessProfile',
        podExecutionRoleArn=fargate_role_arn,
        subnets=subnet_ids,
        selectors=[
            {
                'namespace': 'serverless-apps'
            }
        ]
    )
    print("EKS Fargate Profile creation initiated: ServerlessProfile")

if __name__ == "__main__":
    create_fargate_profile()
