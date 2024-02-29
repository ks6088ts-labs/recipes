import typer
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
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


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
