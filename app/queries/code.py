import os
import uuid
import base64
import requests
from config import CARBON_API

from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, Update, Chat, CallbackQuery
from telegram.ext import CallbackContext, CallbackQueryHandler, ConversationHandler, Filters, MessageHandler

from app.models.telegram_code import TelegramCode
from app.crud.telegram_code import crud_create_telegram_code

from app.messages import start_message


CODE = "CODE_HANDLER"
CODE_INPUT = "CODE_INPUT"
CODE_CANCEL = "CODE_CANCEL"


def code(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    context.user_data['query'] = query

    keyboard = [
        [
            InlineKeyboardButton("❌ Cancelar", callback_data=CODE_CANCEL),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text="Envíame tu código y te devolveré una imagen con la sintaxis resaltada.", reply_markup=reply_markup
    )

    return CODE_INPUT


def code_input(update: Update, context: CallbackContext):
    query: CallbackQuery = context.user_data['query']

    update.message.chat.send_action(action=ChatAction.TYPING, timeout=None)

    code = text = update.message.text

    api_url = f"{CARBON_API}/"

    response = requests.post(api_url, json=dict(code=code))

    if (response.status_code == 200):
        filename = save_file(response.content)

        context.bot.deleteMessage(
            update.message.chat_id, update.message.message_id)

        send_file(filename, update.message.chat)

        query.edit_message_text(text="ℹ️ Listo! 👌")

        update.message.reply_text(f"ℹ️ Misión cumplida {context.user_data['name']}", reply_markup=InlineKeyboardMarkup([
            [code_button],
            [
                InlineKeyboardButton(
                    "👨‍💻 @luis_ciber", url="https://t.me/luis_ciber"),
            ]
        ]))

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


def code_cancel(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    query.edit_message_text(start_message.format(context.user_data['name']), reply_markup=InlineKeyboardMarkup([
        [code_button],
        [
            InlineKeyboardButton(
                "👨‍💻 @luis_ciber", url="https://t.me/luis_ciber"),
        ]
    ]))

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


code_handler = CallbackQueryHandler(code, pattern=f"^{CODE}$")
code_input_handler = MessageHandler(Filters.text, code_input)
code_cancel_handler = CallbackQueryHandler(
    code_cancel, pattern=f"^{CODE_CANCEL}$")

code_button = InlineKeyboardButton(
    text="📺 Generar código", callback_data=str(CODE))
