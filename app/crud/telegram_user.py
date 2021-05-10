import requests
from app.models import TelegramUser
from config import API_URL, API_KEY, API_KEY_NAME


URL = f"{API_URL}/api/v1/telegram_user/"


def crud_create_telegram_user(telegram_user: TelegramUser) -> int:
    response = requests.post(
        URL, json=telegram_user.dict(), headers={API_KEY_NAME: API_KEY})


def get_telegram_user(id: str) -> TelegramUser:
    response = requests.get(
        f"{URL}{id}/", headers={API_KEY_NAME: API_KEY})

    if response.status_code == 200:
        return TelegramUser(**response.json())
