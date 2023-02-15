import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, \
        MessageHandler, filters
from handlers import start, help, allshops, alldiscounts 


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    exit("Specify token env variable")


def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)
    
    all_shops_handler = CommandHandler('allshops', allshops)
    application.add_handler(all_shops_handler)
    
    all_discounts_handler = MessageHandler(
                    filters.TEXT 
                    & (~filters.COMMAND),
                    alldiscounts)
    application.add_handler(all_discounts_handler)
    
    application.run_polling()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
