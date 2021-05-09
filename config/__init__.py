from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT"))
NAME = os.getenv("NAME")

ENVIRONMENT = os.getenv("ENVIRONMENT")

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")

CARBON_API = os.getenv("CARBON_API")
