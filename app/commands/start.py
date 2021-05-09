from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from app.models import TelegramUser
from app.crud.telegram_user import crud_create_telegram_user

start_message = '''
Hola soy TheCoder Bot
'''


def start_handler(update: Update, context: CallbackContext):
    user = TelegramUser(**update.message.from_user.to_dict())

    crud_create_telegram_user(user)

    update.message.reply_text(start_message)


start_command = CommandHandler("start", start_handler)