import requests
from app.models import TelegramCode
from config import API_URL, API_KEY, API_KEY_NAME


URL = f"{API_URL}/api/v1/telegram_code/"


def crud_create_telegram_code(telegram_code: TelegramCode) -> int:
    response = requests.post(
        URL, json=telegram_code.dict(), headers={API_KEY_NAME: API_KEY})


def get_telegram_code(id: str) -> TelegramCode:
    response = requests.get(
        f"{URL}{id}/", headers={API_KEY_NAME: API_KEY})

    if response.status_code == 200:
        return TelegramCode(**response.json())
