# How to run

```bash
# Install dependencies via poetry
❯ poetry install --no-root

# Run the main.py
❯ poetry run python main.py

# query the result
❯ cat ./output.json | jq -r ".[].contents[].title" | grep -e "IoT" -e "AI" --color=always
❯ cat ./output.json | jq -r ".[].contents[]" | grep -e "IoT" -e "AI" --color=always
```

# References

- [非同期処理をシンプルな Python コードで説明する](https://qiita.com/y_kato_eng/items/ca0de5cf1224c807e7e5)
- [How to define array/object in .env file?](https://stackoverflow.com/questions/63846589/how-to-define-array-object-in-env-file)
