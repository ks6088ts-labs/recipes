# Deploy an app in private network

- [microsoft/azurechat](https://github.com/microsoft/azurechat)

## Prerequisites

- Azure subscription

## Deployment

Deploy the following resources in this case:

- Virtual Network
- App Service
- App Service Plan
- Key vault
- Azure OpenAI Service
- Azure Cosmos DB account
- Log Analytics workspace

### Create resources via Azure CLI

Run the following commands to create resources via Azure CLI.

- ref. [Problem generating random string in Azure Cloud Shell Bash](https://learn.microsoft.com/en-us/answers/questions/31353/problem-generating-random-string-in-azure-cloud-sh)
- ref. [Quickstart: Use the Azure CLI to create a virtual network](https://learn.microsoft.com/en-us/azure/virtual-network/quick-create-cli)

```shell
RANDOM_IDENTIFIER=$(head /dev/urandom | tr -dc a-z0-9 | fold -w 5 | head -n 1)
LOCATION="japaneast"
RESOURCE_GROUP_NAME="rg-adhoc-$RANDOM_IDENTIFIER"
VNET_NAME="vnet-$RANDOM_IDENTIFIER"

# Resource group
az group create \
  --name $RESOURCE_GROUP_NAME \
  --location $LOCATION

# Virtual network
az network vnet create \
  --name $VNET_NAME \
  --resource-group $RESOURCE_GROUP_NAME \
  --address-prefix 10.0.0.0/16 \
  --subnet-name "subnet-1" \
  --subnet-prefixes 10.0.0.0/24

az network vnet subnet create \
  --name "subnet-2" \
  --resource-group $RESOURCE_GROUP_NAME \
  --vnet-name $VNET_NAME \
  --address-prefix 10.0.1.0/24

az network vnet subnet create \
  --name "subnet-3" \
  --resource-group $RESOURCE_GROUP_NAME \
  --vnet-name $VNET_NAME \
  --address-prefix 10.0.2.0/24

# Azure OpenAI Service
az cognitiveservices account create \
  --name "aoai-$RANDOM_IDENTIFIER" \
  --resource-group $RESOURCE_GROUP_NAME \
  --location $LOCATION \
  --kind OpenAI \
  --sku s0 \
  --custom-domain "aoai-$RANDOM_IDENTIFIER"

# App Service Plan
az appservice plan create \
  --name "asp-$RANDOM_IDENTIFIER" \
  --resource-group $RESOURCE_GROUP_NAME \
  --location $LOCATION \
  --is-linux \
  --sku P0V3

# App Service
az webapp create \
  --name "app-$RANDOM_IDENTIFIER" \
  --resource-group $RESOURCE_GROUP_NAME \
  --plan "asp-$RANDOM_IDENTIFIER" \
  --https-only true \
  --runtime "node|18-lts" \
  --startup-file "next start"

az webapp config appsettings set \
  --name "app-$RANDOM_IDENTIFIER" \
  --resource-group $RESOURCE_GROUP_NAME \
  --settings \
    AZURE_KEY_VAULT_NAME="kv-$RANDOM_IDENTIFIER" \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true \
    AZURE_OPENAI_VISION_API_KEY=FIXME

# Cosmos DB
az cosmosdb create \
  --name "cosmosdb-$RANDOM_IDENTIFIER" \
  --resource-group $RESOURCE_GROUP_NAME \
  --default-consistency-level Session \
  --locations "regionName=$LOCATION" failoverPriority=0 isZoneRedundant=False \
  --locations regionName=japanwest failoverPriority=1 isZoneRedundant=False

# Key vault
az keyvault create \
  --name "kv-$RANDOM_IDENTIFIER" \
  --resource-group $RESOURCE_GROUP_NAME \
  --location $LOCATION

# # Log Analytics workspace
az monitor log-analytics workspace create \
  --resource-group $RESOURCE_GROUP_NAME \
  --workspace-name "law-$RANDOM_IDENTIFIER"

# For development ----------------------------

# Virtual Machines
az vm create \
  --resource-group $RESOURCE_GROUP_NAME \
  --admin-username azureuser \
  --authentication-type password \
  --name "vm-$RANDOM_IDENTIFIER" \
  --image Ubuntu2204 \
  --public-ip-address ""

# Bastion
az network vnet subnet create \
  --name AzureBastionSubnet \
  --resource-group $RESOURCE_GROUP_NAME \
  --vnet-name $VNET_NAME \
  --address-prefix 10.0.10.0/26

az network public-ip create \
  --resource-group $RESOURCE_GROUP_NAME \
  --name "public-ip-$RANDOM_IDENTIFIER" \
  --sku Standard \
  --location $LOCATION \
  --zone 1 2 3

az network bastion create \
  --name "bastion-$RANDOM_IDENTIFIER" \
  --public-ip-address "public-ip-$RANDOM_IDENTIFIER" \
  --resource-group $RESOURCE_GROUP_NAME \
  --vnet-name $VNET_NAME \
  --location $LOCATION
```

### Set up the private network

Disable the public network access and create a private endpoint for each resource.

- ref. [Azure OpenAI Service にアクセスできるネットワークを制限する](https://techblog.ap-com.co.jp/entry/2023/08/17/120000)
- ref. [【Azure】App Service の VNet 統合とプライベートリンクを利用した通信閉域化](https://techblog.ap-com.co.jp/entry/2021/03/12/150117)

| Resource                       | Document                                                                                                                                                                                                                              | Video                                   |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| Azure OpenAI Service           | [Configure Azure AI services virtual networks](https://learn.microsoft.com/en-us/azure/ai-services/cognitive-services-virtual-networks?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext&tabs=portal#use-private-endpoints) | [YouTube](https://youtu.be/81T5wkaO2V0) |
| App Service                    | [Quickstart: Create a private endpoint by using the Azure portal](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal?tabs=dynamic-ip#create-a-private-endpoint)                                      | [YouTube](https://youtu.be/xIm0TnYMBLQ) |
| App Service (VNET Integration) | [Enable virtual network integration in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/configure-vnet-integration-enable)                                                                                      | [YouTube](https://youtu.be/eaxacB-_PBs) |
| Cosmos DB                      | [Configure Azure Private Link for an Azure Cosmos DB account](https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-configure-private-endpoints?tabs=arm-bicep)                                                                    | [YouTube](https://youtu.be/xWDgN53gXoc) |
| Key Vault                      | [Integrate Key Vault with Azure Private Link](https://learn.microsoft.com/en-us/azure/key-vault/general/private-link-service?tabs=portal)                                                                                             | [YouTube](https://youtu.be/2hA04MPafhA) |

### Set up configurations for App Service

Use role-based access control (RBAC) to grant the app service access to the key vault.
Specifically, assign the `Key Vault Secrets Officer` role to the app service.

- ref. [Use Key Vault references as app settings in Azure App Service and Azure Functions](https://learn.microsoft.com/en-us/azure/app-service/app-service-key-vault-references?tabs=azure-cli)
- ref. [Azure App Service の Key Vault 参照機能を試してみた](https://aadojo.alterbooth.com/entry/2021/03/04/100000)

### Deploy the app

| Steps                                                                         | Document                       | Video                                   |
| ----------------------------------------------------------------------------- | ------------------------------ | --------------------------------------- |
| SSH to the virtual machine inside the private network and confirm connections | -                              | [YouTube](https://youtu.be/bhxRACKMhjI) |
| Use Azure CLI to deploy the app via zip file                                  | see the following descriptions | -                                       |

From a virtual machine, download the app and deploy it.

ref. [.github/workflows/open-ai-app.yml](https://github.com/microsoft/azurechat/blob/main/.github/workflows/open-ai-app.yml)

```shell
az webapp deploy \
  --name $APP_SERVICE_NAME \
  --resource-group $RESOURCE_GROUP_NAME \
  --src-path ./Nextjs-site.zip \
  --type zip
```

### Clean up

```shell
# Resource group
az group delete \
  --name $RESOURCE_GROUP_NAME \
  --yes \
  --no-wait
```

## Notes

Shortest path to deploy azurechat app is to apply the original IaC code and adjust the configurations. If it's not possible, deploy the resources manually and set up the private network as described above.

Tips are as follows:

- To set up Key Vault values, it is recommended to enable public network access for using Azure Portal during the operation to avoid the complexity of the operation.
- Enable public network access for deploying the app during the operation.
