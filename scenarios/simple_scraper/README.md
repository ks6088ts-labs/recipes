# Simple Scraper Tool

This is a simple scraper tool to get the latest articles and save the result as a JSON file.

## Prerequisites

- Python 3.10+
- Poetry
- jq

## How to run

```bash
# Install dependencies via poetry
❯ poetry install --no-root

# ---

# Run sites2json subcommand to get the latest articles and save the result as a JSON file
❯ poetry run python main.py sites2json \
    --env-file-path settings.env.sample \
    --path-to-output-json ./artifacts/items.json

# query the result
❯ cat ./artifacts/items.json | jq -r ".[].contents[].title" | grep -ie "IoT" -ie "AI" --color=always
❯ cat ./artifacts/items.json | jq -r ".[].contents[]"       | grep -ie "IoT" -ie "AI" --color=always

# ---

# Run html2json subcommand to extract the target elements from the HTML file and save the result as a JSON file
❯ poetry run python main.py html2json \
    --xpath "//td[@class='left']/a" \
    --path-to-html ./artifacts/2024.html \
    --path-to-output-json artifacts/2024.json

# query the result
❯ cat ./artifacts/2024.json | jq -r ".[].text"
```

## References

- [非同期処理をシンプルな Python コードで説明する](https://qiita.com/y_kato_eng/items/ca0de5cf1224c807e7e5)
- [How to define array/object in .env file?](https://stackoverflow.com/questions/63846589/how-to-define-array-object-in-env-file)
