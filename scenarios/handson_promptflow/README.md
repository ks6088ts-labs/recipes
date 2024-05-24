# Hands on

- [Quick start](https://microsoft.github.io/promptflow/how-to-guides/quick-start.html)

```shell
# CLI
poetry run pf flow test \
    --flow flow:chat \
    --inputs question="What's the capital of France?"
> Prompt flow service has started...
> You can view the trace detail from the following URL:
> http://127.0.0.1:23333/v1.0/ui/traces/?#collection=handson_promptflow&> uiTraceId=0x7ad420aa1a4f8460f39be501a5115c2c
> The capital of France is Paris.

# SDK
poetry run python flow.py
> Prompt flow service has started...
> You can view the trace detail from the following URL:
> http://127.0.0.1:23333/v1.0/ui/traces/?#collection=handson_promptflow&> uiTraceId=0x23a554e2acc14dc55b4714138cd4b78b
> The capital of France is Paris.

# UI
poetry run pf flow test --flow flow:chat --ui
```

# References

- [Prompt flow を CLI から使ってみる](https://zenn.dev/microsoft/articles/promptflow-cli)
