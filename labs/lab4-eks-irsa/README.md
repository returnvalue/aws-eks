# Lab 4: Security Identity (OIDC & IRSA)

**Goal:** Implement IAM Roles for Service Accounts (IRSA). This prevents pods from sharing the broad permissions of the EC2 node they run on by giving the cluster its own OpenID Connect (OIDC) identity provider.

```bash
# 1. Retrieve the cluster's OIDC Issuer URL
OIDC_URL=$(awslocal eks describe-cluster --name PortfolioCluster --query 'cluster.identity.oidc.issuer' --output text)
echo "Cluster OIDC URL: $OIDC_URL"

# 2. Extract the ID required to register the provider
OIDC_ID=$(basename $OIDC_URL)

# 3. Register the OIDC Provider with AWS IAM
awslocal iam create-open-id-connect-provider \
  --url $OIDC_URL \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 9e99a48a9960b14926bb7f3b02e22da2b0ab7280
```

## 🧠 Key Concepts & Importance

- **IRSA (IAM Roles for Service Accounts):** The preferred way to manage permissions for your applications in EKS. It allows you to associate an IAM role with a Kubernetes service account.
- **OIDC (OpenID Connect):** An identity layer on top of the OAuth 2.0 protocol. EKS uses OIDC to provide an identity to the cluster that IAM can trust.
- **Pod-Level Isolation:** Instead of giving the worker node broad permissions (e.g., access to all S3 buckets), you give each pod only the specific permissions it needs.
- **Least Privilege:** IRSA enforces the principle of least privilege at the application layer, significantly improving the security posture of your cluster.
- **Trust Relationship:** The IAM role's trust policy is configured to trust the OIDC provider and the specific Kubernetes service account.

## 🛠️ Command Reference

- `eks describe-cluster`: Returns descriptive information about an Amazon EKS cluster.
    - `--name`: The name of the cluster.
    - `--query`: Used to extract the OIDC issuer URL.
- `iam create-open-id-connect-provider`: Creates an OIDC provider in IAM.
    - `--url`: The URL of the identity provider.
    - `--client-id-list`: A list of client IDs (typically `sts.amazonaws.com` for IRSA).
    - `--thumbprint-list`: A list of server certificate thumbprints for the OpenID Connect identity provider's server certificate(s).
