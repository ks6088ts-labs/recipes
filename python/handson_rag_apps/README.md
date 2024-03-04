# Simple hands-on for RAG app on Azure

This is a simple hands-on for RAG app on Azure. The following features are implemented:

- Azure OpenAI Service
  - Chat Completion
  - Functions
  - Tools
- Bing Search
  - Search
  - RAG
- Azure AI Search
  - Create index
  - Upload documents
  - Search
  - RAG

Note: [azure-search-documents==11.6.0b1](https://pypi.org/project/azure-search-documents/11.6.0b1/) is used for Azure AI Search.

## Prerequisites

- [Python](https://www.python.org/downloads/) 3.10 or later
- [Poetry](https://python-poetry.org/docs/#installation) (optional)
- [Azure AI Search resource](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search)
- [Azure OpenAI resource](https://learn.microsoft.com/en-us/azure/ai-services/openai/overview)
- [Bing Search resource](https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/create-bing-search-service-resource)

## Setup

### Install dependencies

```shell
# create a virtual environment
python -m venv .venv

# activate the virtual environment
source .venv/bin/activate

# install dependencies to your environment
pip install -r requirements.txt

# or if you use poetry
poetry install --no-root
```

### Setup cloud resources

- Create an Azure AI Search resource and get the key
- Create an Azure OpenAI resource and get the key
- Create a Bing Search resource and get the key

Create a `settings.env` file based on [settings.env.sample](./settings.env.sample) to match your environment. This file is read as environment variables from scripts.

## Azure OpenAI Service

### Help

```shell
❯ python scripts/azure_openai_service.py --help
Usage: azure_openai_service.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  chat-completion
  functions
  tools
```

### Chat Completion

```shell
❯ python scripts/azure_openai_service.py chat-completion --content "日本とオーストラリアの天気を教えて"
ChatCompletion(id='chatcmpl-8uuzgw4LUI9PUa8tLmWJRssOgDykK', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='日本の天気はどこでしょうか、あなたのいる場所を教えていただければ、正確な天気をお伝えできます。\n\nオーストラリアの天気はどこでしょうか、都市名や地域名を教えていただければ、正確な天気をお伝えできます。', role='assistant', function_call=None, tool_calls=None), content_filter_results={'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}})], created=1708576144, model='gpt-35-turbo', object='chat.completion', system_fingerprint='fp_68a7d165bf', usage=CompletionUsage(completion_tokens=102, prompt_tokens=24, total_tokens=126), prompt_filter_results=[{'prompt_index': 0, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}])
```

### Functions

Query the weather in Tokyo, Japan and Sydney, Australia but the response includes just one case (Tokyo, Japan).

```shell
❯ python scripts/azure_openai_service.py functions --content "日本とオーストラリアの天気を教えて"
ChatCompletion(id='chatcmpl-8uuyohsNXcwPqaZH71ZqROO3hRbz5', choices=[Choice(finish_reason='function_call', index=0, logprobs=None, message=ChatCompletionMessage(content=None, role='assistant', function_call=FunctionCall(arguments='{"location":"Tokyo, Japan","unit":"celsius"}', name='get_current_weather'), tool_calls=None), content_filter_results={})], created=1708576090, model='gpt-35-turbo', object='chat.completion', system_fingerprint='fp_68a7d165bf', usage=CompletionUsage(completion_tokens=23, prompt_tokens=91, total_tokens=114), prompt_filter_results=[{'prompt_index': 0, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}])
```

### Tools

Query the weather in Tokyo, Japan and Sydney, Australia and the response includes both cases (Tokyo, Japan and Sydney, Australia).

```shell
❯ python scripts/azure_openai_service.py tools --content "日本とオーストラリアの天気を教えて"
ChatCompletion(id='chatcmpl-8uuzGTqggLLSK0eWN5I9qfPXRXRtr', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_acaztZMjJp0rl0jxzlbt3byM', function=Function(arguments='{"location": "Tokyo, Japan", "unit": "celsius"}', name='get_current_weather'), type='function'), ChatCompletionMessageToolCall(id='call_XNjm0zteIsWbP84Q9nL6YyMx', function=Function(arguments='{"location": "Sydney, Australia", "unit": "celsius"}', name='get_current_weather'), type='function')]), content_filter_results={})], created=1708576118, model='gpt-35-turbo', object='chat.completion', system_fingerprint='fp_68a7d165bf', usage=CompletionUsage(completion_tokens=61, prompt_tokens=91, total_tokens=152), prompt_filter_results=[{'prompt_index': 0, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}])
```

## Bing Search

### Help

```shell
❯ python scripts/bing_search.py --help
Usage: bing_search.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  bing-search
  rag
```

### Search

```shell
❯ python scripts/bing_search.py bing-search --content "最新のプリキュアのタイトルを教えて"
新作プリキュアタイトル発表！ 『わんだふるぷりきゅあ！』は ...
プリキュア新作タイトル発表 21作目は『わんだふるぷりきゅあ ...
「プリキュア」最新作「わんだふるぷりきゅあ！」シリーズ初 ...
【プリキュア】新シリーズのタイトルは『わんだふる ...
「プリキュア」新作タイトルは「わんだふるぷりきゅあ！」初 ...
2024年度新プリキュア タイトル決定！ - アキバ総研
『プリキュア』新シリーズタイトルは『わんだふるぷりきゅあ ...
プリキュア第21弾タイトル「わんだふるぷりきゅあ！」に決定 ...
プリキュアシリーズ最新作『デリシャスパーティ♡プリキュア ...
【新プリキュア】「プリキュア」シリーズ第21弾タイトル決定 ...
```

### RAG

```shell
❯ python scripts/bing_search.py rag --content "最新のプリキュアのタイトルを教えて"
最新のプリキュアのタイトルは「わんだふるぷりきゅあ！」です。
```

## Azure AI Search

Most of the code is based on the [Azure-Samples/azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo) repository.

### Help

```shell
❯ python scripts/azure_ai_search.py --help
Usage: azure_ai_search.py [OPTIONS] COMMAND [ARGS]...

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
❯ python scripts/azure_ai_search.py create-index
```

### Upload documents

```shell
❯ python scripts/azure_ai_search.py upload-documents --documents-csv "./data/documents.csv"
```

### Search

```shell
❯ python scripts/azure_ai_search.py search --query-text "baseball"
{'id': '2', 'content': '河原町二郎は野球が好きです。', 'category': 'test0', 'sourcepage': '2', 'sourcefile': 'sports.pdf', 'search_score': 0.01666666753590107, '@search.reranker_score': 1.5674018859863281}
{'id': '4', 'content': '烏丸四郎はバスケットボールが好きです。', 'category': 'test0', 'sourcepage': '4', 'sourcefile': 'sports.pdf', 'search_score': 0.016393441706895828, '@search.reranker_score': 1.5218290090560913}
{'id': '3', 'content': '寺町三郎は卓球が好きです。', 'category': 'test0', 'sourcepage': '3', 'sourcefile': 'sports.pdf', 'search_score': 0.016129031777381897, '@search.reranker_score': 1.3268994092941284}
```

### RAG

```shell
❯ python scripts/azure_ai_search.py rag --query-text "河原町くんの好きなスポーツは何？"
河原町くんの好きなスポーツは野球です。
❯ python scripts/azure_ai_search.py rag --query-text "ラクロスが好きな人は誰？"
ラクロスが好きな人は、「堀川五郎」です。
```

## References

- [ks6088ts.github.io / Azure 上で作る RAG アプリの基礎](https://ks6088ts.github.io/blog/handson-rag-app)
