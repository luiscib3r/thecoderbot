from config import BOT_TOKEN, PORT, NAME, ENVIRONMENT
from telegram.ext import Updater

from app.commands.start import start_command
from app.commands.code import code_command

if __name__ == "__main__":
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(start_command)
    dp.add_handler(code_command)

    if ENVIRONMENT == "dev":
        updater.start_polling()
        updater.idle()
    else:
        updater.start_webhook(
            listen='0.0.0.0', port=int(PORT), url_path=BOT_TOKEN,
            webhook_url=f"https://{NAME}.herokuapp.com/{BOT_TOKEN}"
        )

        updater.idle()
