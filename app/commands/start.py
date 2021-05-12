from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler

from app.models import TelegramUser
from app.crud.telegram_user import crud_create_telegram_user
from app.messages import start_message

from app.queries.code import code_button, CODE, CODE_INPUT, CODE_CANCEL, code_handler, code_input_handler, code_cancel_handler

INIT = "INIT"


def start_handler(update: Update, context: CallbackContext):
    user = TelegramUser(**update.message.from_user.to_dict())
    context.user_data['name'] = user.x_name

    crud_create_telegram_user(user)

    update.message.reply_text(start_message.format(user.x_name), reply_markup=InlineKeyboardMarkup([
        [code_button],
        [
            InlineKeyboardButton("👨‍💻 @luis_ciber", url="https://t.me/luis_ciber"),
        ]
    ]))

    update.message.delete()

    return INIT


start_command = ConversationHandler(
    entry_points=[
        CommandHandler("start", start_handler),
        code_handler,
    ],
    states={
        INIT: [
            code_handler,
        ],
        CODE_INPUT: [
            code_input_handler,
            code_cancel_handler,
        ]
    },
    fallbacks=[
        CommandHandler("start", start_handler),
    ]
)
