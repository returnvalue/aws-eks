import boto3

# Configure boto3 with localstack endpoint and us-east-1 region
def get_boto3_client(service_name):
    return boto3.client(
        service_name,
        endpoint_url="http://localhost:4566",
        region_name="us-east-1"
    )

eks = get_boto3_client('eks')
iam = get_boto3_client('iam')

def setup_irsa():
    # 1. Retrieve the cluster's OIDC Issuer URL
    print("Fetching cluster OIDC Issuer URL...")
    cluster_info = eks.describe_cluster(name='PortfolioCluster')
    oidc_url = cluster_info['cluster']['identity']['oidc']['issuer']
    print(f"Cluster OIDC URL: {oidc_url}")

    # 2. Register the OIDC Provider with AWS IAM
    print("Registering OIDC Provider with IAM...")
    try:
        iam.create_open_id_connect_provider(
            Url=oidc_url,
            ClientIDList=['sts.amazonaws.com'],
            ThumbprintList=['9e99a48a9960b14926bb7f3b02e22da2b0ab7280']
        )
        print("OIDC Provider created successfully.")
    except iam.exceptions.EntityAlreadyExistsException:
        print("OIDC Provider already exists.")

if __name__ == "__main__":
    setup_irsa()
