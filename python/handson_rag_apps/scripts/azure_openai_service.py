import os

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


@app.command()
def chat_completion(content=DEFAULT_PROMPT):
    client = get_azure_openai_client()
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
def functions(content=DEFAULT_PROMPT):
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

    client = get_azure_openai_client()
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
def tools(content=DEFAULT_PROMPT):
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

    client = get_azure_openai_client()
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
