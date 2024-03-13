# Hands-on AKS

## Create an AKS cluster

- [Quickstart: Deploy an Azure Kubernetes Service (AKS) cluster using Azure CLI](https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-cli)
- [Azure-Samples/aks-store-demo](https://github.com/Azure-Samples/aks-store-demo)

```shell
RESOURCE_GROUP_NAME="rg-handson-aks"
LOCATION="japaneast"
AKS_CLUSTER_NAME="handsonAksCluster"

# Create a resource group
az group create \
  --name $RESOURCE_GROUP_NAME \
  --location $LOCATION

# Create an AKS cluster
az aks create \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $AKS_CLUSTER_NAME \
  --enable-managed-identity \
  --node-count 1 \
  --generate-ssh-keys

# Get the credentials for the AKS cluster
az aks get-credentials \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $AKS_CLUSTER_NAME

# Verify the connection to the AKS cluster
kubectl get nodes

# Deploy an application to the AKS cluster
kubectl apply -f
```

## Deploy an application to the AKS cluster

```shell
# Clone the repository
git clone git@github.com:Azure-Samples/aks-store-demo.git
cd aks-store-demo

# Create a namespace
kubectl create ns pets

# Deploy the application
kubectl apply -f ./aks-store-all-in-one.yaml -n pets

# Verify the deployment
kubectl get service store-front -n pets --watch
```
