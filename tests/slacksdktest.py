import os
from dotenv import load_dotenv
import logging
from slack_sdk import WebClient

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
res = client.api_test()

response = client.chat_postMessage(
    channel="#bme-bot-playground",
    text="Hello, world!"
)
print(response)
