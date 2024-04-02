import os

import typer
from dotenv import load_dotenv
from openai import AzureOpenAI

app = typer.Typer()


# create Azure OpenAI client
def create_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )


# =============================
# Assistants


@app.command()
def create_assistant(
    name="Data Visualization",
    instructions="This assistant helps you to create data visualizations.",
):
    client = create_client()
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        tools=[
            {
                "type": "code_interpreter",
            }
        ],
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT"),
    )
    print(assistant.model_dump_json(indent=2))


@app.command()
def list_assistants():
    client = create_client()
    assistants = client.beta.assistants.list()
    print(assistants.model_dump_json(indent=2))


@app.command()
def delete_assistant(
    assistant_id: str,
):
    client = create_client()
    assistant = client.beta.assistants.delete(
        assistant_id=assistant_id,
    )
    print(assistant.model_dump_json(indent=2))


# =============================
# Assistants / Files


@app.command()
def list_files():
    client = create_client()
    files = client.files.list()
    print(files.model_dump_json(indent=2))


@app.command()
def retrieve_file(
    file_id: str,
):
    client = create_client()
    files = client.files.retrieve(
        file_id=file_id,
    )
    print(files.model_dump_json(indent=2))


@app.command()
def download_image(
    file_id: str,
    output_file="./output.png",
):
    client = create_client()
    content = client.files.content(
        file_id=file_id,
    )
    content.write_to_file(
        file=output_file,
    )


@app.command()
def create_file(
    file_path="./input.pdf",
):
    client = create_client()
    file = client.files.create(
        file=open(file_path, "rb"),
        purpose="assistants",
    )
    print(file.model_dump_json(indent=2))


@app.command()
def delete_file(
    file_id: str,
):
    client = create_client()
    files = client.files.delete(
        file_id=file_id,
    )
    print(files.model_dump_json(indent=2))


# =============================
# Threads


@app.command()
def create_thread():
    client = create_client()
    thread = client.beta.threads.create()
    print(thread.model_dump_json(indent=2))


@app.command()
def retrieve_thread(
    thread_id: str,
):
    client = create_client()
    thread = client.beta.threads.retrieve(
        thread_id=thread_id,
    )
    print(thread.model_dump_json(indent=2))


@app.command()
def delete_thread(
    thread_id: str,
):
    client = create_client()
    thread = client.beta.threads.delete(thread_id=thread_id)
    print(thread.model_dump_json(indent=2))


# =============================
# Threads / Messages


@app.command()
def create_message(
    thread_id: str,
    role="user",
    content="Create a visualization of a sinusoidal wave",
    file_id=None,
):
    client = create_client()
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role=role,
        content=content,
        file_ids=[file_id] if file_id else [],
    )
    print(message.model_dump_json(indent=2))


@app.command()
def list_messages(
    thread_id: str,
):
    client = create_client()
    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
    )
    print(messages.model_dump_json(indent=2))


# =============================
# Threads / Runs


@app.command()
def create_run(
    assistant_id: str,
    thread_id: str,
):
    client = create_client()
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    print(run.model_dump_json(indent=2))


@app.command()
def retrieve_run(
    thread_id: str,
    run_id: str,
):
    client = create_client()
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )
    print(run.model_dump_json(indent=2))


if __name__ == "__main__":
    load_dotenv("./settings.env")

    app()
