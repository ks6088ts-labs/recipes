# Trigger Azure Function with Event Grid

## Deploy the function app to Azure

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

## Link the function app to the Event Grid

To confirm the function app is linked to the Event Grid, run the following commands in the separate terminal windows to run the function app locally.

```shell
# 1. run Azurite
azurite

# 2. launch the function app locally
source .venv/bin/activate
func start

# 3. run ngrok to expose the local function app to the internet
ngrok http 7071
```

As said in the [Manually post the request](https://learn.microsoft.com/en-us/azure/azure-functions/event-grid-how-tos?tabs=v2%2Cportal#manually-post-the-request), set the following webhook URL in the Event Grid subscription from Azure Portal.
`http://{NGROK_URL}/runtime/webhooks/eventgrid?functionName={FUNCTION_NAME}`

### Example: Trigger Azure Function when a new version of the secret in the Key Vault is created

For example, to notify the event of the `Secret New Version Created`, do the following.

- Go to the Azure Portal
- Go to the `Key Vault` > `Events` > `+ Event Subscription`
- Create a new event subscription
  - EVENT TYPES = `Secret New Version Created`
  - Endpoint Type = `Web Hook`
  - Endpoint = `http://{NGROK_URL}/runtime/webhooks/eventgrid?functionName={FUNCTION_NAME}`

Then, the function app should be triggered when a new version of the secret in the Key Vault is created. You can check the logs in the terminal where the function app is running.

To call Azure Function instead of the local function app, replace the event types from webhook to Azure Function.

# References

- [Quickstart: Create a Python function in Azure from the command line](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=linux%2Cbash%2Cazure-cli&pivots=python-mode-decorators)
- [How to work with Event Grid triggers and bindings in Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/event-grid-how-tos?tabs=v2%2Cportal)
