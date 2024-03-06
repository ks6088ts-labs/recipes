import os

import requests
import typer
from dotenv import load_dotenv
from openai import AzureOpenAI

app = typer.Typer()

DEFAULT_PROMPT = "What is the weather like in Boston and New York?"


def get_azure_openai_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=os.getenv("api_key"),
        api_version=os.getenv("api_version"),
        azure_endpoint=os.getenv("azure_endpoint"),
    )


def search(search_term: str) -> str:
    subscription_key = os.getenv("bing_search_key")
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    sources = []
    for search_result in search_results["webPages"]["value"]:
        sources.append(search_result["name"])
    return "\n".join(sources)


@app.command()
def bing_search(content=DEFAULT_PROMPT):
    print(search(content))


@app.command()
def rag(content=DEFAULT_PROMPT):
    sources_str = search(content)
    print(f"got sources: {sources_str}")
    client = get_azure_openai_client()
    messages = [
        {"role": "system", "content": "あなたは優秀なヘルプデスクボットです。"},
        {"role": "user", "content": content + f"\nSources: {sources_str}"},
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
