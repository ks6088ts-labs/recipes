# Hands-on LINE API

## Prerequisites

- [LINE Developers](https://developers.line.biz/ja/)

## Hands-on

### Use official examples

- [line-bot-sdk-python/examples/fastapi-echo](https://github.com/line/line-bot-sdk-python/tree/master/examples/fastapi-echo)

```shell
# Clone the repository
git clone git@github.com:line/line-bot-sdk-python.git
cd line-bot-sdk-python/examples/fastapi-echo

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
pip install -r requirements.txt

# Set the environment variables
export LINE_CHANNEL_SECRET=YOUR_CHANNEL_SECRET
export LINE_CHANNEL_ACCESS_TOKEN=YOUR_CHANNEL_ACCESS_TOKEN
uvicorn main:app --reload

# Run ngrok in the separate terminal window
ngrok http 8000

# Set the webhook URL `https://YOUR_APP.ngrok-free.app/callback` in the LINE Developers Console

# Send a message to the LINE bot
```

### Create a new bot from CLI

```shell
# Install dependencies
poetry install --no-root

# Activate the virtual environment
poetry shell

# Run the server with the reload option
python main.py fastapi-server --port 8000 --reload
```
