import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from events.mention_events import register_mention_events
from events.message_events import register_message_events
from typing import Any, Dict
from slack_bolt.async_app import AsyncApp
from .message_events import MessageEvents
from .mention_events import MentionEvents



def register_events(app: AsyncApp) -> None:
    """Register all event handlers"""
    message_events = MessageEvents(app)
    mention_events = MentionEvents(app)

    # Register message events
    @app.event("message")
    async def handle_message(event: Dict[str, Any], say: Any) -> None:
        await message_events.handle_message(event, say)

    # Register app_mention events
    @app.event("app_mention")
    async def handle_mention(event: Dict[str, Any], say: Any) -> None:
        await mention_events.handle_mention(event, say)

    # Register reaction events
    @app.event("reaction_added")
    async def handle_reaction(event: Dict[str, Any]) -> None:
        await message_events.handle_reaction_added(event)

    return app
