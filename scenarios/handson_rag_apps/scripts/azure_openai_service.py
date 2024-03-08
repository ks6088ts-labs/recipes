import os

import typer
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import AzureOpenAI
from typing_extensions import Annotated

app = typer.Typer()

DEFAULT_PROMPT = "What is the weather like in Boston and New York?"


def get_azure_openai_client(use_ms_entra_id=False) -> AzureOpenAI:
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


@app.command()
def chat_completion(
    content=DEFAULT_PROMPT,
    use_ms_entra_id: Annotated[
        bool, typer.Option(help="Use Microsoft Entra ID.")
    ] = False,
):
    client = get_azure_openai_client(use_ms_entra_id)
    chat_completion = client.chat.completions.create(
        model=os.getenv("azure_deployment_gpt"),
        messages=[
            {
                "role": "user",
                "content": content,
            },
        ],
    )
    print(chat_completion)


@app.command()
def functions(
    content=DEFAULT_PROMPT,
    use_ms_entra_id: Annotated[
        bool, typer.Option(help="Use Microsoft Entra ID.")
    ] = False,
):
    functions = []
    functions.append(
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    )

    client = get_azure_openai_client(use_ms_entra_id)
    chat_completion = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=[
            {
                "role": "user",
                "content": content,
            },
        ],
        functions=functions,
    )
    print(chat_completion)


@app.command()
def tools(
    content=DEFAULT_PROMPT,
    use_ms_entra_id: Annotated[
        bool, typer.Option(help="Use Microsoft Entra ID.")
    ] = False,
):
    tools = []
    tools.append(
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
    )

    client = get_azure_openai_client(use_ms_entra_id)
    chat_completion = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=[
            {
                "role": "user",
                "content": content,
            },
        ],
        tools=tools,
    )

    print(chat_completion)


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
