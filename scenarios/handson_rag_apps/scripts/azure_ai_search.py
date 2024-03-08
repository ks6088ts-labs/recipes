import asyncio
import os

import typer
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents.aio import SearchClient
from azure.search.documents.indexes.aio import SearchIndexClient
from azure.search.documents.indexes.models import (
    AzureOpenAIParameters,
    AzureOpenAIVectorizer,
    HnswAlgorithmConfiguration,
    HnswParameters,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
    SimpleField,
    VectorSearch,
    VectorSearchProfile,
)
from azure.search.documents.models import (
    QueryLanguage,
    QuerySpellerType,
    QueryType,
    VectorizedQuery,
)
from dotenv import load_dotenv
from openai import AzureOpenAI
from typing_extensions import Annotated

app = typer.Typer()


def get_fields() -> list:
    return [
        SimpleField(name="id", type="Edm.String", key=True),
        SearchableField(
            name="content",
            type="Edm.String",
            analyzer_name="ja.lucene",
        ),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            hidden=False,
            searchable=True,
            filterable=False,
            sortable=False,
            facetable=False,
            vector_search_dimensions=1536,
            vector_search_profile_name="embedding_config",
        ),
        SimpleField(
            name="category", type="Edm.String", filterable=True, facetable=True
        ),
        SimpleField(
            name="sourcepage",
            type="Edm.String",
            filterable=True,
            facetable=True,
        ),
        SimpleField(
            name="sourcefile",
            type="Edm.String",
            filterable=True,
            facetable=True,
        ),
    ]


def get_index_name() -> str:
    return os.getenv("index_name")


def get_index(index_name: str, fields: list) -> SearchIndex:
    return SearchIndex(
        name=index_name,
        fields=fields,
        semantic_search=SemanticSearch(
            configurations=[
                SemanticConfiguration(
                    name="default",
                    prioritized_fields=SemanticPrioritizedFields(
                        title_field=None,
                        content_fields=[SemanticField(field_name="content")],
                    ),
                )
            ]
        ),
        vector_search=VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(
                    name="hnsw_config",
                    parameters=HnswParameters(metric="cosine"),
                )
            ],
            profiles=[
                VectorSearchProfile(
                    name="embedding_config",
                    algorithm_configuration_name="hnsw_config",
                    vectorizer=f"{index_name}-vectorizer",
                ),
            ],
            vectorizers=[
                AzureOpenAIVectorizer(
                    name=f"{index_name}-vectorizer",
                    kind="azureOpenAI",
                    azure_open_ai_parameters=AzureOpenAIParameters(
                        resource_uri=os.getenv("azure_endpoint"),
                        deployment_id=os.getenv("azure_deployment_embedding"),
                        api_key=os.getenv("api_key"),
                    ),
                ),
            ],
        ),
    )


def get_azure_search_index_client(use_ms_entra_id: bool) -> SearchIndexClient:
    if use_ms_entra_id:
        return SearchIndexClient(
            endpoint=os.getenv("azure_search_endpoint"),
            credential=DefaultAzureCredential(),
        )
    return SearchIndexClient(
        endpoint=os.getenv("azure_search_endpoint"),
        credential=AzureKeyCredential(os.getenv("azure_search_key")),
    )


def get_azure_search_client(index_name: str, use_ms_entra_id: bool) -> SearchClient:
    if use_ms_entra_id:
        return SearchClient(
            endpoint=os.getenv("azure_search_endpoint"),
            index_name=index_name,
            credential=DefaultAzureCredential(),
        )
    return SearchClient(
        endpoint=os.getenv("azure_search_endpoint"),
        index_name=index_name,
        credential=AzureKeyCredential(os.getenv("azure_search_key")),
    )


def get_azure_openai_client(use_ms_entra_id) -> AzureOpenAI:
    if use_ms_entra_id:
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )
        return AzureOpenAI(
            api_version=os.getenv("api_version"),
            azure_endpoint=os.getenv("azure_endpoint"),
            azure_ad_token_provider=token_provider,
        )
    return AzureOpenAI(
        api_key=os.getenv("api_key"),
        api_version=os.getenv("api_version"),
        azure_endpoint=os.getenv("azure_endpoint"),
    )


def load_csv(path_to_csv: str) -> list:
    import csv

    with open(path_to_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(
            f,
            delimiter=",",
        )
        documents = [row for row in reader]
        return documents


async def create_index_impl(index: SearchIndex, use_ms_entra_id: bool):
    async with get_azure_search_index_client(use_ms_entra_id) as search_index_client:
        await search_index_client.create_index(index)


async def upload_documents_impl(
    index_name: str, path_to_csv: str, use_ms_entra_id: bool
):
    aoai_client = get_azure_openai_client(use_ms_entra_id)
    documents = load_csv(path_to_csv=path_to_csv)
    async with get_azure_search_client(index_name, use_ms_entra_id) as search_client:
        embeddings = aoai_client.embeddings.create(
            input=[document["content"] for document in documents],
            model=os.getenv("azure_deployment_embedding"),
        )
        for i, document in enumerate(documents):
            document["embedding"] = embeddings.data[i].embedding

        await search_client.upload_documents(documents)


async def search_impl(query_text: str, index_name: str, use_ms_entra_id: bool):
    aoai_client = get_azure_openai_client(use_ms_entra_id)
    embeddings = aoai_client.embeddings.create(
        input=query_text,
        model=os.getenv("azure_deployment_embedding"),
    )
    query_vector = embeddings.data[0].embedding

    async with get_azure_search_client(index_name, use_ms_entra_id) as search_client:
        results = await search_client.search(
            search_text=query_text,
            query_type=QueryType.SEMANTIC,
            query_language=QueryLanguage.JA_JP,
            query_speller=QuerySpellerType.NONE,
            semantic_configuration_name="default",
            top=3,
            vector_queries=[
                VectorizedQuery(
                    vector=query_vector,
                    k_nearest_neighbors=50,
                    fields="embedding",
                ),
            ],
        )
        documents = []
        async for page in results.by_page():
            async for document in page:
                documents.append(
                    {
                        "id": document["id"],
                        "content": document["content"],
                        "category": document["category"],
                        "sourcepage": document["sourcepage"],
                        "sourcefile": document["sourcefile"],
                        "search_score": document["@search.score"],
                        "@search.reranker_score": document["@search.reranker_score"],
                    }
                )
        return documents


@app.command()
def create_index(
    use_ms_entra_id: Annotated[
        bool, typer.Option(help="Use Microsoft Entra ID.")
    ] = False,
):
    fields = get_fields()
    index_name = get_index_name()
    index = get_index(
        index_name=index_name,
        fields=fields,
    )
    asyncio.run(create_index_impl(index, use_ms_entra_id))


@app.command()
def upload_documents(
    documents_csv="documents.csv",
    use_ms_entra_id: Annotated[
        bool, typer.Option(help="Use Microsoft Entra ID.")
    ] = False,
):
    index_name = get_index_name()
    asyncio.run(
        upload_documents_impl(
            index_name=index_name,
            path_to_csv=documents_csv,
            use_ms_entra_id=use_ms_entra_id,
        )
    )


@app.command()
def search(
    query_text="basketball",
    use_ms_entra_id: Annotated[
        bool, typer.Option(help="Use Microsoft Entra ID.")
    ] = False,
):
    index_name = get_index_name()
    documents = asyncio.run(
        search_impl(
            query_text=query_text,
            index_name=index_name,
            use_ms_entra_id=use_ms_entra_id,
        )
    )
    for document in documents:
        print(document)


@app.command()
def rag(
    query_text="河原町さんの好きなスポーツは何ですか？",
    use_ms_entra_id: Annotated[
        bool, typer.Option(help="Use Microsoft Entra ID.")
    ] = False,
):
    index_name = get_index_name()
    documents = asyncio.run(
        search_impl(
            query_text=query_text,
            index_name=index_name,
            use_ms_entra_id=use_ms_entra_id,
        )
    )
    sources = []
    for document in documents:
        sources.append(document["content"])
    sources_str = "\n".join(sources)
    print(f"got sources: {sources_str}")
    client = get_azure_openai_client(use_ms_entra_id)
    messages = [
        {"role": "system", "content": "あなたは優秀なヘルプデスクボットです。"},
        {"role": "user", "content": query_text + f"\nSources: {sources_str}"},
    ]

    chat_completion = client.chat.completions.create(
        model=os.getenv("azure_deployment_gpt"),
        messages=messages,
    )
    print(chat_completion.choices[0].message.content)


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
