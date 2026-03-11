# Lab 5: Cluster Add-ons Management (VPC CNI)

**Goal:** EKS clusters rely on operational software (Add-ons) like the VPC CNI (for networking) and CoreDNS. Manage these natively through the AWS API to ensure they are updated and patched alongside the cluster control plane.

```bash
# Install the Amazon VPC CNI add-on directly via the EKS API
awslocal eks create-addon \
  --cluster-name PortfolioCluster \
  --addon-name vpc-cni \
  --addon-version v1.18.0-eksbuild.1
```

## 🧠 Key Concepts & Importance

- **EKS Add-ons:** Curated operational software that provides supporting capabilities to Kubernetes clusters. They are managed directly by AWS, simplifying the cluster lifecycle.
- **Amazon VPC CNI:** A Kubernetes Container Network Interface (CNI) plugin that provides native VPC networking for your pods. It allows pods to have the same IP address inside the pod as they do on the VPC network.
- **Managed Lifecycle:** By using the EKS Add-on API, AWS handles the installation, updates, and health monitoring of these critical components.
- **Version Compatibility:** EKS ensures that the add-on versions are compatible with your specific Kubernetes version, reducing the risk of broken clusters during upgrades.
- **Standardization:** Add-ons provide a standardized way to deploy core cluster services like CoreDNS, kube-proxy, and the VPC CNI.

## 🛠️ Command Reference

- `eks create-addon`: Installs an Amazon EKS add-on.
    - `--cluster-name`: The name of the cluster.
    - `--addon-name`: The name of the add-on (e.g., `vpc-cni`).
    - `--addon-version`: The specific version of the add-on to install.
