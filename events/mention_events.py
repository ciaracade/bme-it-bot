# When responding to an @, what is the bot doing??

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# User mentions the robot
def register_mention_events(app):

    # handle_app_greeting is when the user is greeting the robot.
    @app.event("app_mention")
    def handle_app_greeting(event, say):
        user = event["user"]
        text = event["text"].lower()

        if "hello" in text or "hi" in text:
            say(f"Hi there, <@{user}>! I'm here to help. Do you have any questions?")
    
    # handle_deleted_message_events logs when a message is deleted
    @app.event("message")
    def handle_deleted_message_events(event, logger):
        if event.get("subtype") == "message_deleted":
            logger.info("Message deleted event received")

    return app