import boto3
import os
import subprocess

# Configure the EKS client for LocalStack
# Note: update-kubeconfig is typically a CLI-specific helper, 
# but we can simulate the intent or use the underlying logic.
# In a real boto3 scenario, you'd manage the config file manually or via subprocess.

def solution():
    print("Updating kubeconfig for PortfolioCluster...")
    # Since update-kubeconfig is a complex CLI command that modifies local files,
    # the most direct 'boto3-like' or programmatic way in this context is to 
    # invoke the CLI command via subprocess if we want the actual file update.
    try:
        subprocess.run([
            "awslocal", "eks", "update-kubeconfig", 
            "--name", "PortfolioCluster", 
            "--region", "us-east-1"
        ], check=True)
        print("Kubeconfig updated successfully.")
    except Exception as e:
        print(f"Error updating kubeconfig: {e}")

if __name__ == "__main__":
    solution()
