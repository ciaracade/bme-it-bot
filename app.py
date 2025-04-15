from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import requests # using requests for now, no need for somethign more like flask 
import os

# Initializes your app with your bot token and socket mode handler
load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# TBR
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()