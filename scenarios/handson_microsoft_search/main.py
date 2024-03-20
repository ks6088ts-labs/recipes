import asyncio
import os

import typer
from azure.identity.aio import ClientSecretCredential, OnBehalfOfCredential
from dotenv import load_dotenv
from kiota_abstractions.api_error import APIError
from msgraph import GraphServiceClient
from msgraph.generated.models.entity_type import EntityType
from msgraph.generated.models.search_query import SearchQuery
from msgraph.generated.models.search_request import SearchRequest
from msgraph.generated.search.query.query_post_request_body import \
    QueryPostRequestBody
from msgraph.generated.search.query.query_post_response import \
    QueryPostResponse

app = typer.Typer()


def get_graph_service_client(
    scopes=["https://graph.microsoft.com/.default"],
) -> GraphServiceClient:
    credential = ClientSecretCredential(
        tenant_id=os.getenv("tenant_id"),
        client_id=os.getenv("client_id"),
        client_secret=os.getenv("client_secret"),
    )
    return GraphServiceClient(credentials=credential, scopes=scopes)


def get_on_behalf_of_graph_service_client(
    token: str,
    scopes=["https://graph.microsoft.com/.default"],
) -> GraphServiceClient:
    credential = OnBehalfOfCredential(
        tenant_id=os.getenv("tenant_id"),
        client_id=os.getenv("client_id"),
        client_secret=os.getenv("client_secret"),
        user_assertion=token,
    )
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
def search(
    token="your_token",
    query="your_query",
):
    client = get_on_behalf_of_graph_service_client(token=token)

    # POST /search/query
    # Permission: Sites.Read.All
    async def search():
        try:
            response: QueryPostResponse = await client.search.query.post(
                body=QueryPostRequestBody(
                    requests=[
                        SearchRequest(
                            entity_types=[EntityType.ListItem],
                            query=SearchQuery(
                                query_string=query,
                            ),
                            size=3,
                        )
                    ]
                )
            )
            print(response.__str__)
        except APIError as e:
            print(f"Error: {e.error.message}")

    asyncio.run(search())


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
