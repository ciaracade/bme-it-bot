import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

try:
    response = client.chat_postMessage(
        channel='#bme-bot-playground', text="Beamy the BME Bot is all set up! 🚀")
    assert response["message"]["text"] == "Beamy the BME Bot is all set up! :rocket:"
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")
    # Also receive a corresponding status_code
    assert isinstance(e.response.status_code, int)
    print(f"Received a response status_code: {e.response.status_code}")

# From Slack Python SDK API documentation
