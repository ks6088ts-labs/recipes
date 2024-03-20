# hands on Microsoft Graph API

- [Use the Microsoft Graph API](https://learn.microsoft.com/en-us/graph/use-the-api)
- [訳あって Microsoft Graph API 調べてみた](https://qiita.com/massie_g/items/fe7540161aa4a5f86bf5)

## curl

```shell
CLIENT_ID="<type your settings>"
CLIENT_SECRET="<type your settings>"

# get tenant id
TENANT_ID=$(az account show --query tenantId --output tsv)

# get access token
ACCESS_TOKEN=$(curl -s -X POST "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "client_id=$CLIENT_ID" \
    -d "client_secret=$CLIENT_SECRET" \
    -d "grant_type=client_credentials" \
    -d "scope=https%3A%2F%2Fgraph.microsoft.com%2F.default" | jq -r .access_token)

# call graph api
USER_OBJECT_ID="<type your settings>"
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    "https://graph.microsoft.com/v1.0/users/$USER_OBJECT_ID" | jq -r .
```

## Python

```shell
# Help
❯ poetry run python main.py --help
---
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  get-user
  search

# get-user
❯ poetry run python main.py get-user <USER_ID>
---
user_principal_name: hello@world.onmicrosoft.com, display_name: YOUR_NAME, id: USER_ID

# search
❯ poetry run python main.py search --help
Usage: main.py search [OPTIONS]

Options:
  --token TEXT  [default: your_token]
  --query TEXT  [default: your_query]
  --help        Show this message and exit.
```

# References

- [Office365 Graph で 2 種類のアクセス許可の仕様にハマった話 #o365jp](https://speakerdeck.com/sugimomoto/office365-graph-de2zhong-lei-falseakusesuxu-ke-falseshi-yang-nihamatutahua-number-o365jp)
- [Microsoft Graph REST API v1.0 エンドポイント リファレンス](https://learn.microsoft.com/ja-jp/graph/api/overview?view=graph-rest-1.0)
- [Microsoft Graph PowerShell SDK を使用したライセンス管理操作の紹介 > サービス プリンシパル（アプリケーション）を使用する方法](https://jpazureid.github.io/blog/azure-active-directory/operating-license-with-microsoft-graph/#idx2-2)
- [07JP27/azureopenai-internal-microsoft-search](https://github.com/07JP27/azureopenai-internal-microsoft-search/blob/main/src/backend/core/graphclientbuilder.py)
- [OpenAI と Microsoft Graph Search API で M365 の組織内データを検索する RAG アプリを作る](https://zenn.dev/microsoft/articles/azure-openai-graph-rag-pattern)
