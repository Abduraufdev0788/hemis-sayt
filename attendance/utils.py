import requests
from core.settings import BOT_TOKEN

BOT_TOKEN = BOT_TOKEN

def send_telegram(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text
    }

    requests.post(url, data=data)