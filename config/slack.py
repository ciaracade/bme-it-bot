import os
from dotenv import load_dotenv
from slack_bolt import App
from events.register_events import register_events

def connect_slack():

    load_dotenv()

    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

    app = App(token=SLACK_BOT_TOKEN)

    register_events(app) # Register Slack events for bot 

    return app
        
