import openai
import os
from slack_bolt.adapter.socket_mode import SocketModeHandler
from config.slack import connect_slack
from flask import Flask
from slack_sdk import WebClient
from config.slack import connect_slack

app = connect_slack()

if __name__ == "__main__":
    SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    print("Beamy the BME Bot is running!")
    handler.start()

