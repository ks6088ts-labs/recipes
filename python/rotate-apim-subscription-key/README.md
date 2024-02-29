# Rotate subscription keys for API Management

## Prerequisites

- Python

## Setup

### Create an Azure service principal with Azure CLI

- [Create an Azure service principal with Azure CLI](https://learn.microsoft.com/en-us/cli/azure/azure-cli-sp-tutorial-1?tabs=bash)
- [Service Principal az cli login failing - NO subscriptions found](https://stackoverflow.com/questions/55457349/service-principal-az-cli-login-failing-no-subscriptions-found)

```shell
servicePrincipalName="your-sp-name"
roleName="contributor"
subscriptionID=$(az account show --query id --output tsv)
# Verify the ID of the active subscription
echo "Using subscription ID $subscriptionID"
resourceGroup="your-rg-name"

echo "Creating SP for RBAC with name $servicePrincipalName, with role $roleName and in scopes /subscriptions/$subscriptionID/resourceGroups/$resourceGroup"
az ad sp create-for-rbac --name $servicePrincipalName --role $roleName --scopes /subscriptions/$subscriptionID/resourceGroups/$resourceGroup

# {
#   "appId": "your-app-id",
#   "displayName": "your-display-name",
#   "password": "your-password",
#   "tenant": "your-tenant-id"
# }
```

### Use an Azure service principal with password-based authentication

- [Use an Azure service principal with password-based authentication](https://learn.microsoft.com/en-us/cli/azure/azure-cli-sp-tutorial-2)

```shell
az login --service-principal \
         --username $appId \
         --password $password \
         --tenant $tenant
```

### Assign roles to the service principal

- [Unable to create secrets in Azure Key Vault if using Azure role-based access control](https://stackoverflow.com/a/69971679)

## Usage

### Help

```shell
❯ python main.py --help
```

### Set KeyVault secret

```shell
❯ python main.py set-key-vault-secret \
  --key-vault-name "name" \
  --key-vault-secret-name "secret-name" \
  --key-vault-secret-value "secret-value"
```

### Get KeyVault secret

```shell
❯ python main.py get-key-vault-secret \
  --key-vault-name "name" \
  --key-vault-secret-name "secret-name" \
  --key-vault-secret-version "00000000"
```

# References

- [Quickstart: Azure Key Vault secret client library for Python](https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python?tabs=azure-cli)
- [How to auto rotate an API subscription key in Azure](https://learn.microsoft.com/en-us/answers/questions/963672/how-to-auto-rotate-an-api-subscription-key-in-azur)
