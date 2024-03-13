from enum import Enum

import typer
import uvicorn
from dotenv import load_dotenv
from typing_extensions import Annotated

app = typer.Typer()


class LogLevel(str, Enum):
    critical = "critical"
    error = "error"
    warning = "warning"
    info = "info"
    debug = "debug"


@app.command()
def fastapi_server(
    host="127.0.0.1",
    port: int = 8080,
    log_level: LogLevel = LogLevel.info,
    reload: Annotated[bool, typer.Option(help="Enable auto-reload.")] = False,
):
    uvicorn.run(
        "fastapi_app:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )


@app.command()
def run():
    print("hello")


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
