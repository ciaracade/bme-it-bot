# When listening to a message, what is the bot doing??
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

def register_message_events(app):

    @app.message(":wave:")
    def handle_wave(message, say):
        user = message['user']
        say(f"Hi there, <@{user}>! :wave::skin-tone-5:")

    return app
