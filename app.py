import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# VARIABLES
DEBUG = True;
PORT = int(os.environ.get('PORT', '8443'))

# DEBUG o PRODUCCION
if DEBUG:
    TOKEN = "TOKEN_BOT_DEBUG"
else:
    TOKEN = "TOKEN_NOT_PRODUCTION"


# Login del bot
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Inicio de bot
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Ready!')

# Ayuda del bot
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('La ayuda no esta disponible pongase en contacto con @PekenoSalta')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if DEBUG:
        updater.start_polling()
    else:  
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN) 
        updater.bot.set_webhook("HEROKU_URL" + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()
