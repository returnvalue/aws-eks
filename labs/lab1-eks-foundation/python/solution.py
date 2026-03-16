import boto3
import json

# Configure boto3 with localstack endpoint and us-east-1 region
def get_boto3_client(service_name):
    return boto3.client(
        service_name,
        endpoint_url="http://localhost:4566",
        region_name="us-east-1"
    )

ec2 = get_boto3_client('ec2')
iam = get_boto3_client('iam')
eks = get_boto3_client('eks')

def create_eks_foundation():
    # 1. Create VPC and Subnets
    print("Creating VPC...")
    vpc_response = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id = vpc_response['Vpc']['VpcId']
    print(f"Created VPC: {vpc_id}")

    print("Creating Subnets...")
    subnet1_response = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock='10.0.1.0/24',
        AvailabilityZone='us-east-1a'
    )
    subnet1_id = subnet1_response['Subnet']['SubnetId']
    print(f"Created Subnet 1: {subnet1_id}")

    subnet2_response = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock='10.0.2.0/24',
        AvailabilityZone='us-east-1b'
    )
    subnet2_id = subnet2_response['Subnet']['SubnetId']
    print(f"Created Subnet 2: {subnet2_id}")

    # 2. Create the EKS Cluster Service Role
    print("Creating IAM Role for EKS...")
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": {"Service": "eks.amazonaws.com"}, "Action": "sts:AssumeRole"}]
    }
    
    role_response = iam.create_role(
        RoleName='EKSClusterRole',
        AssumeRolePolicyDocument=json.dumps(trust_policy)
    )
    cluster_role_arn = role_response['Role']['Arn']
    print(f"Created IAM Role: {cluster_role_arn}")

    # 3. Create the EKS Cluster
    print("Creating EKS Cluster...")
    eks.create_cluster(
        name='PortfolioCluster',
        roleArn=cluster_role_arn,
        resourcesVpcConfig={
            'subnetIds': [subnet1_id, subnet2_id]
        }
    )
    print("EKS Cluster creation initiated: PortfolioCluster")

if __name__ == "__main__":
    create_eks_foundation()
