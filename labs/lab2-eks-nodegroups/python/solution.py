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

def create_managed_nodegroup():
    # 1. Create the Node IAM Role
    print("Creating IAM Role for EKS Nodes...")
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": {"Service": "ec2.amazonaws.com"}, "Action": "sts:AssumeRole"}]
    }
    
    role_response = iam.create_role(
        RoleName='EKSNodeRole',
        AssumeRolePolicyDocument=json.dumps(trust_policy)
    )
    node_role_arn = role_response['Role']['Arn']
    print(f"Created IAM Role: {node_role_arn}")

    # To make this script work independently, we should fetch the subnet IDs from the existing cluster
    print("Fetching cluster details to get subnets...")
    cluster_info = eks.describe_cluster(name='PortfolioCluster')
    subnet_ids = cluster_info['cluster']['resourcesVpcConfig']['subnetIds']
    print(f"Found subnets: {subnet_ids}")

    # 2. Create the Managed Node Group
    print("Creating EKS Managed Node Group...")
    eks.create_nodegroup(
        clusterName='PortfolioCluster',
        nodegroupName='StandardCompute',
        nodeRole=node_role_arn,
        subnets=subnet_ids,
        instanceTypes=['t3.medium'],
        scalingConfig={
            'minSize': 1,
            'maxSize': 3,
            'desiredSize': 2
        }
    )
    print("EKS Node Group creation initiated: StandardCompute")

if __name__ == "__main__":
    create_managed_nodegroup()
