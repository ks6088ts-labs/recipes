# Event Grid Triggered Azure Functions

## Deployment

```shell
# https://learn.microsoft.com/en-us/answers/questions/31353/problem-generating-random-string-in-azure-cloud-sh
RANDOM_IDENTIFIER=$(head /dev/urandom | tr -dc a-z0-9 | fold -w 5 | head -n 1)
RESOURCE_GROUP_NAME="rg-$RANDOM_IDENTIFIER"
REGION="japaneast"
STORAGE_ACCOUNT_NAME="sa$RANDOM_IDENTIFIER"
FUNCTION_APP_NAME="fa$RANDOM_IDENTIFIER"

# https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=linux%2Cbash%2Cazure-cli&pivots=python-mode-decorators#create-supporting-azure-resources-for-your-function
az login

az group create \
    --name $RESOURCE_GROUP_NAME \
    --location $REGION

az storage account create \
    --name $STORAGE_ACCOUNT_NAME \
    --location $REGION \
    --resource-group $RESOURCE_GROUP_NAME \
    --sku Standard_LRS

az functionapp create \
    --resource-group $RESOURCE_GROUP_NAME \
    --consumption-plan-location $REGION \
    --runtime python \
    --runtime-version "3.11" \
    --functions-version 4 \
    --name $FUNCTION_APP_NAME \
    --os-type linux \
    --storage-account $STORAGE_ACCOUNT_NAME

func azure functionapp publish $FUNCTION_APP_NAME

# To delete the resources
# az group delete --name $RESOURCE_GROUP_NAME --yes --no-wait
```

# References

- [Quickstart: Create a Python function in Azure from the command line](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=linux%2Cbash%2Cazure-cli&pivots=python-mode-decorators)
- [How to work with Event Grid triggers and bindings in Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/event-grid-how-tos?tabs=v2%2Cportal)
