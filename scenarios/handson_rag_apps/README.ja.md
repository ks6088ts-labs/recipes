# Azure 上の RAG アプリのシンプルなハンズオン

これは Azure 上の RAG アプリのシンプルなハンズオンです。以下の機能が実装されています：

- Azure OpenAI Service
  - Chat Completion
  - Functions
  - Tools
- Bing 検索
  - 検索
  - RAG
- Azure AI Search
  - インデックスの作成
  - ドキュメントのアップロード
  - 検索
  - RAG

本ハンズオンは [ks6088ts-labs/recipes](https://github.com/ks6088ts-labs/recipes/blob/main/scenarios/handson_rag_apps/README.md) に基づいています。

Note: Azure AI Search の SDK は [azure-search-documents==11.6.0b1](https://pypi.org/project/azure-search-documents/11.6.0b1/) が使われています。

## 事前条件

- [Python](https://www.python.org/downloads/) 3.10 以上
- [Poetry](https://python-poetry.org/docs/#installation) (optional)
- [Azure AI Search resource](https://learn.microsoft.com/ja-jp/azure/search/search-what-is-azure-search)
- [Azure OpenAI resource](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/overview)
- [Bing Search resource](https://learn.microsoft.com/ja-jp/bing/search-apis/bing-web-search/create-bing-search-service-resource)

## セットアップ

### 依存関係のインストール

```shell
# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化
source .venv/bin/activate
# Windows の場合
.venv\Scripts\Activate

# ライブラリのインストール
pip install -r requirements.txt

# poretry を使う場合
poetry install --no-root
```

### Azure リソースのセットアップ

- Azure AI Search リソースを作成し、キーを取得します
- Azure OpenAI リソースを作成し、キーを取得します
- Bing Search リソースを作成し、キーを取得します

環境に合わせて、[settings.env.sample](./settings.env.sample) を元に `settings.env` ファイルを作成してください。このファイルはスクリプトから環境変数として読み込まれます。

## Azure OpenAI Service

Azure OpenAI Service の API をサービスプリンシパル認証で呼び出すには、サービスプリンシパルを作成し、サービスプリンシパルに `Cognitive Services OpenAI User` ロールを割り当てる必要があります。

- [リソースにアクセスできる Microsoft Entra アプリケーションとサービス プリンシパルを作成する](https://learn.microsoft.com/ja-jp/entra/identity-platform/howto-create-service-principal-portal)
- [Python を使用して OpenAI エンドポイントと Azure OpenAI エンドポイントを切り替える方法](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/how-to/switching-endpoints#microsoft-entra-id-authentication)
- [Azure OpenAI Service のロールベースのアクセス制御](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/how-to/role-based-access-control)

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

❯ python scripts/azure_openai_service.py chat-completion --content "日本とオーストラリアの天気を教えて" --use-ms-entra-id
ChatCompletion(id='chatcmpl-90KYx2k6ZAOVlGDNnHo2XFsXnT8qK', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='申し訳ありませんが、現在の具体的な日本とオーストラリアの天気情報を提供することはできません。天候情報は頻繁に変化するため、最新の情報は天気予報サイトや天気アプリをご利用ください。', role='assistant', function_call=None, tool_calls=None), content_filter_results={'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}})], created=1709866071, model='gpt-35-turbo', object='chat.completion', system_fingerprint=None, usage=CompletionUsage(completion_tokens=90, prompt_tokens=24, total_tokens=114), prompt_filter_results=[{'prompt_index': 0, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}])
```

### Functions

日本とオーストラリアの天気を聞いていますが、日本のケースについての関数呼び出しのみが返っています。Functions は仕様上、一回の呼び出しでは単一の関数呼び出しに制限されます。

```shell
❯ python scripts/azure_openai_service.py functions --content "日本とオーストラリアの天気を教えて"
ChatCompletion(id='chatcmpl-8uuyohsNXcwPqaZH71ZqROO3hRbz5', choices=[Choice(finish_reason='function_call', index=0, logprobs=None, message=ChatCompletionMessage(content=None, role='assistant', function_call=FunctionCall(arguments='{"location":"Tokyo, Japan","unit":"celsius"}', name='get_current_weather'), tool_calls=None), content_filter_results={})], created=1708576090, model='gpt-35-turbo', object='chat.completion', system_fingerprint='fp_68a7d165bf', usage=CompletionUsage(completion_tokens=23, prompt_tokens=91, total_tokens=114), prompt_filter_results=[{'prompt_index': 0, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}])
```

### Tools

日本とオーストラリアの天気を聞いていますが、日本とオーストラリアの天気についての回答が返ってきます。Tools は仕様上、一回の呼び出しで複数の関数呼び出しを行うことができます。

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

検索結果としてはほぼ最新のプリキュアタイトルの情報が返っていますが、一部旧作のプリキュアの情報も含まれています。

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

Bing 単体の検索結果として一部旧作のプリキュアの情報も含まれていましたが、RAG による回答では最新のプリキュアタイトルの情報が返っています。

```shell
❯ python scripts/bing_search.py rag --content "最新のプリキュアのタイトルを教えて"
最新のプリキュアのタイトルは「わんだふるぷりきゅあ！」です。
```

## Azure AI Search

ほとんどのコードは[Azure-Samples/azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo)リポジトリに基づいています。

Azure AI Search の API をサービスプリンシパル認証で呼び出すには、サービスプリンシパルを作成し、サービスプリンシパルに `Search Index Data Reader` ロールを割り当てる必要があります。

- [Python 用 Azure Cognitive Search クライアント ライブラリ - バージョン 11.4.0](https://learn.microsoft.com/en-us/python/api/overview/azure/search-documents-readme?view=azure-python#create-a-client-using-microsoft-entra-id-authentication)

### Help

```shell
❯ python scripts/azure_ai_search.py --help
Usage: azure_ai_search.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified
                                  shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell,
                                  to copy it or customize the
                                  installation.
  --help                          Show this message and exit.

Commands:
  create-index
  rag
  search
  upload-documents
```

### Create index

```shell
❯ python scripts/azure_ai_search.py create-index
❯ python scripts/azure_ai_search.py create-index --use-ms-entra-id
```

### Upload documents

一般に公開されていないデータを扱うシナリオを想定して、架空の情報を記載した CSV ファイルを作成して Azure AI Search にデータをアップロードします。

```shell
❯ python scripts/azure_ai_search.py upload-documents --documents-csv "./data/documents.csv"
```

### Search

Azure AI Search に対して検索を行います。

```shell
❯ python scripts/azure_ai_search.py search --query-text "baseball"
{'id': '2', 'content': '河原町二郎は野球が好きです。', 'category': 'test0', 'sourcepage': '2', 'sourcefile': 'sports.pdf', 'search_score': 0.01666666753590107, '@search.reranker_score': 1.5674018859863281}
{'id': '4', 'content': '烏丸四郎はバスケットボールが好きです。', 'category': 'test0', 'sourcepage': '4', 'sourcefile': 'sports.pdf', 'search_score': 0.016393441706895828, '@search.reranker_score': 1.5218290090560913}
{'id': '3', 'content': '寺町三郎は卓球が好きです。', 'category': 'test0', 'sourcepage': '3', 'sourcefile': 'sports.pdf', 'search_score': 0.016129031777381897, '@search.reranker_score': 1.3268994092941284}
```

### RAG

架空の情報を記載した CSV ファイルを使って RAG による回答を行います。Azure AI Search に登録した情報を元に適切な回答が返ってきます。

```shell
❯ python scripts/azure_ai_search.py rag --query-text "河原町くんの好きなスポーツは何？"
河原町くんの好きなスポーツは野球です。
❯ python scripts/azure_ai_search.py rag --query-text "ラクロスが好きな人は誰？"
ラクロスが好きな人は、「堀川五郎」です。
```

## References

- [ks6088ts.github.io / Azure 上で作る RAG アプリの基礎](https://ks6088ts.github.io/blog/handson-rag-app)
