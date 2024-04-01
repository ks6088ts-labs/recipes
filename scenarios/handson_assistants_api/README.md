# Hands-on Assistants API

## Overview

Refer to the following docs to get started with Azure OpenAI Assistants (Preview):

- [Assistants support](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/assistant#assistants-support)
- [Azure OpenAI Service models](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#assistants-preview) about the supported models and regions.
- Supported models: `gpt-35-turbo (0613)`+, `gpt-4 (0613)`+
- API version: `2024-02-15-preview`+

## Prerequisites

Copy [settings.env.sample](./settings.env.sample) to `settings.env` and set your credentials.

## How to run

```shell
# Install dependencies
poetry install

# Help
poetry run python main.py --help

# Create a new assistant
poetry run python main.py create-assistant

# List all assistants and get the assistant ID
poetry run python main.py list-assistants | jq -r ".data[].id"

# Delete an assistant
poetry run python main.py delete-assistant $ASSISTANT_ID

# Create a new thread
poetry run python main.py create-thread

# List all threads and get the thread ID
poetry run python main.py retrieve-thread $THREAD_ID

# Delete a thread
poetry run python main.py delete-thread $THREAD_ID

# Create a message to a thread
poetry run python main.py create-message $THREAD_ID

# List all messages in a thread
poetry run python main.py list-messages $THREAD_ID

# Create a run
poetry run python main.py create-run $ASSISTANT_ID $THREAD_ID

# Retrieve a run
poetry run python main.py retrieve-run $THREAD_ID $RUN_ID

# Note: need to call `list-messages` to confirm the generated file id

# List files
poetry run python main.py list-files

# Retrieve a file
poetry run python main.py retrieve-file $FILE_ID

# Download a file
poetry run python main.py download-image $FILE_ID --output-file ./output.png

# Create a file
poetry run python main.py create-file --file-path ./output.png

# Delete a file
poetry run python main.py delete-file $FILE_ID
```

## Use cases

### Analyze CSV data

```shell
FILE=./data/titanic.csv

# Download the Titanic dataset
curl -o $FILE "https://gist.githubusercontent.com/jwalsh/ce1dc0436aba5b7a5c9666f47fa5a380/raw/5ce3854392b43ff97907112d344fc008229b0445/titanic.csv"

# Create a file
poetry run python main.py create-file --file-path $FILE
# See the response and set the file ID `.id`
FILE_ID=assistant-xxx

# Create a new assistant
poetry run python main.py create-assistant \
    --name "CSV Analyzer" \
    --instructions "Analyze the content of the CSV file. Provide a summary of the data."
# See the response and set the assistant ID `.id`
ASSISTANT_ID=asst_xxx

# Create a new thread
poetry run python main.py create-thread
THREAD_ID=thread_xxx

# Create a message to a thread
poetry run python main.py create-message $THREAD_ID \
    --role "user" \
    --content "添付ファイルの解析をした結果を教えてください。" \
    --file-id $FILE_ID

# Create a run
poetry run python main.py create-run $ASSISTANT_ID $THREAD_ID
RUN_ID="run_xxx"

# Retrieve a run to confirm status
poetry run python main.py retrieve-run $THREAD_ID $RUN_ID

# See the results
poetry run python main.py list-messages $THREAD_ID
```

## References

- [Getting started with Azure OpenAI Assistants (Preview)](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/assistant)
- [Assistants API (Preview) reference](https://learn.microsoft.com/en-us/azure/ai-services/openai/assistants-reference?tabs=python)
- [Assistants API (Preview) threads reference](https://learn.microsoft.com/en-us/azure/ai-services/openai/assistants-reference-threads?tabs=python)
- [Assistants API (Preview) messages reference](https://learn.microsoft.com/en-us/azure/ai-services/openai/assistants-reference-messages?tabs=python)
- [Assistants API (Preview) runs reference](https://learn.microsoft.com/en-us/azure/ai-services/openai/assistants-reference-runs?tabs=python)
- [Azure OpenAI Assistants Code Interpreter (Preview)](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/code-interpreter?tabs=python)
