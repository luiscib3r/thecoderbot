import requests
from app.models import TelegramMessage
from config import API_URL, API_KEY, API_KEY_NAME


URL = f"{API_URL}/api/v1/telegram_message/"


def crud_create_telegram_message(telegram_message: TelegramMessage) -> int:
    response = requests.post(
        URL, json=telegram_message.dict(), headers={API_KEY_NAME: API_KEY})


def get_telegram_message(id: str) -> TelegramMessage:
    response = requests.get(
        f"{URL}{id}/", headers={API_KEY_NAME: API_KEY})

    if response.status_code == 200:
        return TelegramMessage(**response.json())
