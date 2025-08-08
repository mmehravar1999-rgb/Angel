#!/usr/bin/env python3
"""
Main entry point for the Telegram bot.
This file initializes and runs the bot with proper error handling and logging.
"""

import logging
import sys
from telegram.ext import Application

from bot.config import Config
from bot.handlers import setup_handlers

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main function to initialize and run the bot."""
    try:
        # Load configuration
        config = Config()
        
        if not config.telegram_token:
            logger.error("TELEGRAM_BOT_TOKEN is not set. Please check your environment variables.")
            sys.exit(1)
        
        # Create application
        application = Application.builder().token(config.telegram_token).build()
        
        # Setup handlers
        setup_handlers(application)
        
        logger.info("Starting bot...")
        
        # Run the bot
        application.run_polling(allowed_updates=["message", "callback_query"])
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
