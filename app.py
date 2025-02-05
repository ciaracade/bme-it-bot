import os
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode import SocketModeHandler
from events.register_events import register_events
from handlers.register_commands import register_commands
from config.settings import get_settings

settings = get_settings()

app = AsyncApp(
    token=settings.SLACK_BOT_TOKEN,
    signing_secret=settings.SLACK_SIGNING_SECRET
)

# Register command handlers
register_commands(app)

# Register event handlers
register_events(app)

if __name__ == "__main__":
    handler = SocketModeHandler(app, settings.SLACK_APP_TOKEN)
    handler.start()
    print("Beamy the BME Bot is running!")

