# When listening to a message, what is the bot doing??
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from handlers.base_handler import BaseHandler
from services.openai_service import OpenAIService
from typing import Any, Dict
from slack_bolt.async_app import AsyncApp
import logging

def register_message_events(app):

    @app.message(":wave:")
    def handle_wave(message, say):
        user = message['user']
        say(f"Hi there, <@{user}>! :wave::skin-tone-3:")

    return app

class MessageEventHandler(BaseHandler):
    def __init__(self, app):
        self.ai_service = OpenAIService()
        super().__init__(app)
    
    def register_handlers(self, app):
        app.event("message")(self.handle_message)
        app.event("app_mention")(self.handle_mention)
    
    async def handle_message(self, message, say):
        """Handle direct messages to the bot"""
        try:
            # Don't respond to bot messages
            if message.get("subtype") == "bot_message":
                return

            response = await self.ai_service.get_completion(
                f"Respond to this IT support question: {message['text']}"
            )
            await say(response)

        except Exception as e:
            await self.handle_error(e, say)

    async def handle_mention(self, event, say):
        """Handle when the bot is mentioned"""
        try:
            text = event['text'].replace(f"<@{event['bot_id']}>", "").strip()
            response = await self.ai_service.get_completion(
                f"Respond to this IT support mention: {text}"
            )
            await say(response)
            
        except Exception as e:
            await self.handle_error(e, say)

class MessageEvents:
    def __init__(self, app: AsyncApp):
        self.app = app
        self.openai_service = OpenAIService()

    async def handle_message(self, event: Dict[str, Any], say: Any) -> None:
        """Handle direct messages to the bot"""
        try:
            # Don't respond to bot messages or threads
            if event.get('bot_id') or event.get('thread_ts') or event.get("subtype") == "bot_message":
                return

            # Handle direct messages
            if event.get('channel_type') == 'im':
                message = event.get('text', '').strip()
                if message:
                    response, _ = await self.openai_service.get_completion(
                        f"Respond to this IT support question: {message}"
                    )
                    await say(response)

        except Exception as e:
            logging.error(f"Error handling message event: {e}")
            await say("Sorry, I encountered an error processing your message.")

    async def handle_reaction_added(self, event: Dict[str, Any]) -> None:
        """Handle reactions added to messages"""
        try:
            if event.get('reaction') == 'thumbsup':
                message_ts = event.get('item', {}).get('ts')
                channel = event.get('item', {}).get('channel')
                if message_ts and channel:
                    logging.info(f"Message {message_ts} in {channel} marked as helpful")
                    # Could add feedback to solution database here

        except Exception as e:
            logging.error(f"Error handling reaction event: {e}")
