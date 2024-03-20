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

# Delete the cluster
az group delete \
  --name $RESOURCE_GROUP_NAME \
  --yes --no-wait
```

## Deploy taskapp

- [Monorepo of task management application](https://github.com/gihyodocker/taskapp)
- [Docker/Kubernetes 実践コンテナ開発入門 改訂新版](https://gihyo.jp/book/2024/978-4-297-14017-5)

```shell
# alias k=kubectl

# Display contexts from kubeconfig
k config get-contexts

# Set the current-context in a kubeconfig file
k config use-context handsonAksCluster

# Display nodes
k get nodes

# Display cluster information
k cluster-info

# Clone the repository
git clone https://github.com/gihyodocker/taskapp
cd taskapp

make make-mysql-passwords
make make-k8s-mysql-secret

make api-config.yaml
make make-k8s-api-config

# Local
docker compose up -d --build
curl http://localhost:9280/

# AKS
cd k8s/plain/aks
k apply -f mysql-secret.yaml
k apply -f api-config-secret.yaml
k apply -f mysql.yaml
k apply -f migrator.yaml
k apply -f api.yaml
k apply -f web.yaml # if it doesn't work, use LoadBalancer instead of Ingress. ref. https://github.com/Azure-Samples/aks-store-demo/blob/main/aks-store-all-in-one.yaml#L407

k get ingress web
curl http://$ADDRESS
```
