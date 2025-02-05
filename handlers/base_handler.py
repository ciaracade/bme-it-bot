from abc import ABC, abstractmethod
from slack_bolt.async_app import AsyncApp

class BaseHandler(ABC):
    def __init__(self, app: AsyncApp):
        self.app = app
        self.register_handlers(app)
    
    @abstractmethod
    def register_handlers(self, app: AsyncApp):
        """Register all handlers for this class"""
        pass
    
    async def handle_error(self, error, say):
        """Common error handling"""
        await say(f"❌ Error: {str(error)}") 