import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from events.mention_events import register_mention_events
from events.message_events import register_message_events



def register_events(app):
    register_mention_events(app)
    register_message_events(app)
    
    return app
