import requests
import sys
import os

sys.path.append(os.getcwd())

from config import CARBON_API

api_url = f"{CARBON_API}/"

response = requests.post(api_url, json=dict(code="sas"))
