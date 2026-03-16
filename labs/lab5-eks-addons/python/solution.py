import boto3

# Configure boto3 with localstack endpoint and us-east-1 region
def get_boto3_client(service_name):
    return boto3.client(
        service_name,
        endpoint_url="http://localhost:4566",
        region_name="us-east-1"
    )

eks = get_boto3_client('eks')

def create_addon():
    # 1. Install the Amazon VPC CNI add-on directly via the EKS API
    print("Creating EKS Add-on: vpc-cni...")
    try:
        eks.create_addon(
            clusterName='PortfolioCluster',
            addonName='vpc-cni',
            addonVersion='v1.18.0-eksbuild.1'
        )
        print("EKS Add-on creation initiated: vpc-cni")
    except eks.exceptions.ResourceInUseException:
        print("Add-on vpc-cni is already in use or being created.")

if __name__ == "__main__":
    create_addon()
