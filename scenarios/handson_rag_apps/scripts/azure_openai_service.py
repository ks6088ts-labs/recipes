import base64
import os
from urllib.parse import urljoin

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


def get_gpt4v_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=os.getenv("api_key"),
        api_version=os.getenv("api_version"),
        base_url=urljoin(
            os.getenv("azure_endpoint"),
            f"openai/deployments/{os.getenv('azure_deployment_gpt4v')}/extensions",
        ),
    )


def get_extra_body(use_vision_enhancements):
    if not use_vision_enhancements:
        return None
    return {
        "dataSources": [
            {
                "type": "AzureComputerVision",
                "parameters": {
                    "endpoint": os.getenv("azure_cv_endpoint"),
                    "key": os.getenv("azure_cv_api_key"),
                },
            }
        ],
        "enhancements": {"ocr": {"enabled": True}, "grounding": {"enabled": True}},
    }


@app.command()
def chat_completion(
    content=DEFAULT_PROMPT,
    use_ms_entra_id: Annotated[
        bool, typer.Option(help="Use Microsoft Entra ID.")
    ] = False,
    stream: Annotated[bool, typer.Option(help="Use stream option")] = False,
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
        stream=stream,
    )

    if stream:
        for chunk in chat_completion:
            print(chunk)
            print("****************")
    else:
        print(chat_completion)


@app.command()
def functions(
    content=DEFAULT_PROMPT,
    use_ms_entra_id: Annotated[
        bool, typer.Option(help="Use Microsoft Entra ID.")
    ] = False,
    stream: Annotated[bool, typer.Option(help="Use stream option")] = False,
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
        stream=stream,
    )

    if stream:
        for chunk in chat_completion:
            print(chunk)
            print("****************")
    else:
        print(chat_completion)


@app.command()
def tools(
    content=DEFAULT_PROMPT,
    use_ms_entra_id: Annotated[
        bool, typer.Option(help="Use Microsoft Entra ID.")
    ] = False,
    stream: Annotated[bool, typer.Option(help="Use stream option")] = False,
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
        stream=stream,
    )

    if stream:
        for chunk in chat_completion:
            print(chunk)
            print("****************")
    else:
        print(chat_completion)


@app.command()
def gpt4v_chat_completion(
    content="Please describe the following input image in Japanese in detail.",
    image_path="./data/contoso-allinone.jpg",
    use_vision_enhancements: Annotated[
        bool, typer.Option(help="Use vision enhancements for the image.")
    ] = False,
):
    client = get_gpt4v_client()
    encoded_image = base64.b64encode(open(image_path, "rb").read()).decode("ascii")
    response = client.chat.completions.create(
        model=os.getenv("azure_deployment_gpt4v"),
        messages=[
            {
                "role": "system",
                "content": "You are a top quality image scanning machine.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": content,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                    },
                ],
            },
        ],
        max_tokens=2000,
        extra_body=get_extra_body(use_vision_enhancements),
    )
    print(f"raw response: {response}")
    print("/" * 80)
    print(f"extracted content: {response.choices[0].message.content}")


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
