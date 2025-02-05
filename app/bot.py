from slack_bolt.async_app import AsyncApp
from config.settings import get_settings
from handlers.ticket_handlers import TicketHandler
from handlers.help_handler import HelpHandler

def create_app():
    """Create and configure the Slack bot application"""
    settings = get_settings()
    
    app = AsyncApp(
        token=settings.SLACK_BOT_TOKEN,
        signing_secret=settings.SLACK_SIGNING_SECRET
    )
    
    # Initialize handlers
    TicketHandler(app)
    HelpHandler(app)
    
    return app 