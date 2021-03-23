from tele import chat_id, bot, token

from app import blockchain, chains

from telegram.ext import Updater
from telegram.ext import CommandHandler

# updater
updater = Updater(token=token, use_context=True)


dispatcher = updater.dispatcher

# Command handler


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=blockchain)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
