# Lab 7: Connecting to the Cluster (kubeconfig)

**Goal:** Generate the local configuration file required by `kubectl` to authenticate with the EKS API server and manage Kubernetes resources.

```bash
# Generate and update the local kubeconfig file
awslocal eks update-kubeconfig \
  --name PortfolioCluster \
  --region us-east-1
```

## 🧠 Key Concepts & Importance

- **kubeconfig:** A file used to configure access to Kubernetes clusters. It contains cluster details, certificates, and authentication tokens.
- **kubectl Integration:** `kubectl` uses the kubeconfig file to find the information it needs to choose a cluster and communicate with the API server of that cluster.
- **Contexts:** Kubeconfig files can contain multiple "contexts," allowing you to easily switch between different clusters (e.g., dev, staging, prod) or different users.
- **Authentication:** For EKS, the kubeconfig usually invokes the AWS CLI (or `awslocal`) to generate a temporary token for authentication, ensuring that Kubernetes access is tied to IAM permissions.
- **API Server Communication:** Once configured, you can use standard Kubernetes commands (e.g., `kubectl get pods`, `kubectl apply`) to manage your serverless or node-based workloads.

## 🛠️ Command Reference

- `eks update-kubeconfig`: Configures `kubectl` to communicate with your EKS cluster.
    - `--name`: The name of the EKS cluster.
    - `--region`: The AWS region where the cluster is located.
