import logging
from slack_bolt.async_app import AsyncApp
from app.constants import ERROR_MESSAGES

def register_middleware(app: AsyncApp):
    @app.middleware
    async def log_request(logger, body, next):
        """Log incoming requests"""
        logger.debug(f"Incoming request: {body}")
        return await next()

    @app.error
    async def handle_errors(error, body, logger):
        """Global error handler"""
        logger.error(f"Error: {error}")
        logger.error(f"Request body: {body}")
        
        # Map known error types to user-friendly messages
        error_message = ERROR_MESSAGES.get(
            type(error).__name__,
            "An unexpected error occurred. Please try again later."
        )
        
        if hasattr(body, 'channel'):
            await app.client.chat_postMessage(
                channel=body['channel'],
                text=f"❌ {error_message}"
            ) 