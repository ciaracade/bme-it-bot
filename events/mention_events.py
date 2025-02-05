# When responding to an @, what is the bot doing??
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from typing import Any, Dict
from slack_bolt.async_app import AsyncApp
from services.openai_service import OpenAIService
from services.teamdynamix_tickets import TeamDynamixTickets
import re
import logging

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

class MentionEvents:
    def __init__(self, app: AsyncApp):
        self.app = app
        self.openai_service = OpenAIService()
        self.tdx_tickets = TeamDynamixTickets()

    async def handle_mention(self, event: Dict[str, Any], say: Any) -> None:
        """Handle mentions of the bot"""
        try:
            message = event.get('text', '').strip()
            user = event.get('user')
            
            # Remove the bot mention from the message
            message = re.sub(r'<@[A-Z0-9]+>', '', message).strip()

            if not message:
                await say(f"Hi <@{user}>! How can I help you?")
                return

            # Check for ticket-related questions
            if any(word in message.lower() for word in ['ticket', 'issue', 'problem']):
                ticket_id_match = re.search(r'#?(\d+)', message)
                if ticket_id_match:
                    ticket_id = ticket_id_match.group(1)
                    ticket = await self.tdx_tickets.get_ticket(ticket_id)
                    if ticket:
                        response = (
                            f"📝 Ticket #{ticket['ID']}\n"
                            f"Status: {ticket['Status']}\n"
                            f"Title: {ticket['Title']}\n"
                            f"Created: {ticket['CreatedDate']}"
                        )
                        await say(response)
                        return

            # Get AI response for other queries
            response, _ = await self.openai_service.get_completion(
                f"Respond to this IT support mention: {message}"
            )
            await say(response)

        except Exception as e:
            logging.error(f"Error handling mention event: {e}")
            await say("Sorry, I encountered an error processing your request.")