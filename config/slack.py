import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


def connect_slack():

    load_dotenv()

    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

    app = App(token=SLACK_BOT_TOKEN)

    # will move app events to another lcoation
    @app.event("app_mention")
    def handle_app_mention(event, say):
        user = event["user"]
        say(f"Hi there, <@{user}>! Beamy the BME Bot is ready to assist. 🚀")

    # test example
    @app.event("message")
    def send_greeting(event, say):
        if "hello" in event.get("text", "").lower():
            say("Hi there! 👋 Beamy the BME Bot is here to help!")

    return app
        
