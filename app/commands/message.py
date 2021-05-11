from telegram import ChatAction, Update
from telegram.ext import CallbackContext, MessageHandler, Filters

from datetime import datetime

from app.crud.telegram_message import crud_create_telegram_message
from app.models import TelegramMessage


def message(update: Update, context: CallbackContext):
    update.message.chat.send_action(action=ChatAction.TYPING, timeout=None)

    message = TelegramMessage(
        id=update.message.message_id,
        text=update.message.text,
        chat_id=update.message.chat.id,
        from_id=update.message.from_user.id,
        date=update.message.date.strftime("%Y-%m-%d %H:%M:%S")
    )

    crud_create_telegram_message(message)

    context.bot.deleteMessage(update.message.chat_id,
                              update.message.message_id)

    update.message.reply_text(
        "Si está intentando generar código resaltado debe usar el comando /code antes de enviar su código.")


message_handler = MessageHandler(Filters.text, message)
