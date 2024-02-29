import typer
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.apimanagement import ApiManagementClient
from dotenv import load_dotenv

app = typer.Typer()


@app.command()
def set_key_vault_secret(
    key_vault_name: str = "name",
    key_vault_secret_name: str = "secret-name",
    key_vault_secret_value: str = "secret-value",
):
    credential = DefaultAzureCredential()
    key_vault_secret_client = SecretClient(
        vault_url=f"https://{key_vault_name}.vault.azure.net",
        credential=credential,
    )
    secret = key_vault_secret_client.set_secret(
        name=key_vault_secret_name,
        value=key_vault_secret_value,
    )
    print(f"{secret.name} created successfully!")


@app.command()
def get_key_vault_secret(
    key_vault_name: str = "name",
    key_vault_secret_name: str = "secret-name",
    key_vault_secret_version=None,
):
    credential = DefaultAzureCredential()
    key_vault_secret_client = SecretClient(
        vault_url=f"https://{key_vault_name}.vault.azure.net",
        credential=credential,
    )
    secret = key_vault_secret_client.get_secret(
        name=key_vault_secret_name,
        version=key_vault_secret_version,
    )
    print(
        f"got {key_vault_secret_name}:{key_vault_secret_version} = {secret.value} successfully!"
    )


@app.command()
def regenerate_api_management_primary_key(
    subscription_id: str = "subscription-id",
    resource_group_name: str = "resource-group-name",
    api_management_name: str = "api-management-name",
    api_management_subscription_id: str = "api-management-subscription-id",
):
    client = ApiManagementClient(
        credential=DefaultAzureCredential(), subscription_id=subscription_id
    )
    # regenerate primary key
    client.subscription.regenerate_primary_key(
        resource_group_name=resource_group_name,
        service_name=api_management_name,
        sid=api_management_subscription_id,
    )
    print("regenerated primary key successfully!")


@app.command()
def list_api_management_secrets(
    subscription_id: str = "subscription-id",
    resource_group_name: str = "resource-group-name",
    api_management_name: str = "api-management-name",
    api_management_subscription_id: str = "api-management-subscription-id",
):
    client = ApiManagementClient(
        credential=DefaultAzureCredential(), subscription_id=subscription_id
    )
    # list secrets
    response = client.subscription.list_secrets(
        resource_group_name=resource_group_name,
        service_name=api_management_name,
        sid=api_management_subscription_id,
    )
    print(f"listed secrets successfully! {response}")


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
