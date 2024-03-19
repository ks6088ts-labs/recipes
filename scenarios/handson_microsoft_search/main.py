import asyncio
import os

import typer
from azure.identity.aio import ClientSecretCredential
from dotenv import load_dotenv
from kiota_abstractions.api_error import APIError
from msgraph import GraphServiceClient

app = typer.Typer()


def get_graph_service_client() -> GraphServiceClient:
    credential = ClientSecretCredential(
        tenant_id=os.getenv("tenant_id"),
        client_id=os.getenv("client_id"),
        client_secret=os.getenv("client_secret"),
    )
    scopes = ["https://graph.microsoft.com/.default"]
    return GraphServiceClient(credentials=credential, scopes=scopes)


@app.command()
def get_user(
    user_id: str,
):
    client = get_graph_service_client()

    # GET /users/{id | userPrincipalName}
    async def get_user():
        try:
            user = await client.users.by_user_id(user_id).get()
            print(
                f"user_principal_name: {user.user_principal_name}, display_name: {user.display_name}, id: {user.id}"
            )
        except APIError as e:
            print(f"Error: {e.error.message}")

    asyncio.run(get_user())


@app.command()
def search():
    get_graph_service_client()
    assert False, "Not implemented"


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
