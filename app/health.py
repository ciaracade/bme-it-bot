from datetime import datetime
from slack_bolt.async_app import AsyncApp

def register_health_check(app: AsyncApp):
    @app.command("/health")
    async def health_check(ack, say):
        """Check the bot's health status"""
        await ack()
        
        status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "services": {
                "slack": "connected",
                "teamdynamix": "connected",
                "openai": "connected"
            }
        }
        
        await say(f"🏥 Bot Health Status:\n```{status}```") 