import os
import uuid
import requests
from config import CARBON_API
from telegram import ChatAction, Update, Chat
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, Filters, MessageHandler
from app.models.telegram_code import TelegramCode
from app.crud.telegram_code import crud_create_telegram_code
import base64

CODE_INPUT = 0


def code_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Envíame tu código y te devolveré una imagen con la sintaxis resaltada.'
    )

    return CODE_INPUT


def code_input_text(update: Update, context: CallbackContext):
    code = text = update.message.text

    api_url = f"{CARBON_API}/"

    response = requests.post(api_url, json=dict(code=code))

    if (response.status_code == 200):
        filename = save_file(response.content)

        context.bot.deleteMessage(update.message.chat_id, update.message.message_id)

        send_file(filename, update.message.chat)

        code = TelegramCode(
            id=update.message.message_id,
            text=update.message.text,
            chat_id=update.message.chat.id,
            from_id=update.message.from_user.id,
            date=update.message.date.strftime("%Y-%m-%d %H:%M:%S"),
            image=base64.b64encode(open(filename, "rb").read())
        )

        crud_create_telegram_code(code)

        os.unlink(filename)
    else:
        update.message.reply_text(
            "Ocurrión un error al generar la imagen para el código")

    return ConversationHandler.END


def save_file(file: bytes):
    filename = f"{str(uuid.uuid1())}.png"

    open(filename, 'wb').write(file)

    return filename


def send_file(filename: str, chat: Chat):
    chat.send_action(action=ChatAction.UPLOAD_PHOTO, timeout=None)

    chat.send_photo(
        photo=open(filename, 'rb')
    )


code_command = ConversationHandler(
    entry_points=[
        CommandHandler("code", code_handler)
    ],
    states={
        CODE_INPUT: [
            MessageHandler(Filters.text, code_input_text)
        ],
    },
    fallbacks=[]
)
