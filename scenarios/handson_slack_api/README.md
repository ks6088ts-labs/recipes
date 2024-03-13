# Hands-on Slack API

## Prerequisites

- [Slack API / Apps](https://api.slack.com/apps)

## Hands-on

### curl

```shell
# OAuth & Permissions > OAuth Tokens for Your Workspace
SLACK_API_TOKEN="YOUR_SLACK_API_TOKEN"
# Invite the bot to a channel
CHANNEL_NAME="YOUR_CHANNEL_NAME"

# Post message to Slack
curl -X POST \
    -H "Authorization: Bearer ${SLACK_API_TOKEN}" \
    -H "Content-type: application/json" \
    --data "{\"text\" : \"Hello World\", \"channel\" : \"${CHANNEL_NAME}\"}" \
    "https://slack.com/api/chat.postMessage" -vvvv
```

### Use official examples

- [slackapi/bolt-python](https://github.com/slackapi/bolt-python)
- [Slack App の作り方を丁寧に残す【Bot と Event API の設定編】](https://zenn.dev/mokomoka/articles/6d281d27aa344e)

```shell
# Clone the repository
git clone git@github.com:slackapi/bolt-python.git
cd bolt-python/examples/fastapi

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install slack_bolt

# Set the environment variables
export SLACK_SIGNING_SECRET=***
export SLACK_BOT_TOKEN=xoxb-***

# Run the server with the reload option
uvicorn app:api --reload --port 3000 --log-level warning

# Run ngrok in the separate terminal window
ngrok http 3000
```
