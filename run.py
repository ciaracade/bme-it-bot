from app.bot import create_app
import asyncio
from utils.logger import setup_logging

if __name__ == "__main__":
    # Setup logging
    setup_logging()
    
    # Create and run the bot
    app = create_app()
    asyncio.run(app.start()) 