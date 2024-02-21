# Azure AI Search client CLI written in Python

This is a CLI to create an index, upload documents, and query the index for Azure AI Search. The Python client library for Azure AI Search is [azure-search-documents==11.6.0b1](https://pypi.org/project/azure-search-documents/11.6.0b1/).

## Prerequisites

- Python 3.10 or later
- Azure AI Search resource
- Azure OpenAI resource
- [Poetry](https://python-poetry.org/docs/#installation)

## Setup

### Install dependencies

```shell
# using poetry
poetry install
```

### Setup cloud resources

- Create an Azure AI Search resource and get the key
- Create an Azure OpenAI resource and get the key

Create a `settings.env` file based on [settings.env.sample](./settings.env.sample) to match your environment. This file is read as environment variables from the [main.py](./main.py) script.

## Usage

### Help

```shell
❯ poetry run python main.py --help
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  create-index
  search
  upload-documents
```

### Create index

```shell
❯ poetry run python main.py create-index
```

### Upload documents

```shell
❯ poetry run python main.py upload-documents --documents-csv "./documents.csv"
```

### Search

```shell
❯ poetry run python main.py search --query-text "baseball"
{'id': '2', 'content': '河原町二郎は野球が好きです。', 'category': 'test0', 'sourcepage': '2', 'sourcefile': 'sports.pdf', 'search_score': 0.01666666753590107, '@search.reranker_score': 1.5674018859863281}
{'id': '3', 'content': '堀川五郎はラクロスが好きです。', 'category': 'test1', 'sourcepage': '5', 'sourcefile': 'sports.pdf', 'search_score': 0.016129031777381897, '@search.reranker_score': 1.318857192993164}
{'id': '1', 'content': '東大路太郎はサッカーが好きです。', 'category': 'test0', 'sourcepage': '1', 'sourcefile': 'sports.pdf', 'search_score': 0.016393441706895828, '@search.reranker_score': 1.2035845518112183}
```

## References

- [Azure-Samples/azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo)
