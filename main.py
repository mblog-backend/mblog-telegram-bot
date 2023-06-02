import urllib3
urllib3.disable_warnings()
import requests
import time
from config import TELEGRAM_TOKEN, proxies
from telegram_api import process_telegram_message

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    requests.post(f"{BASE_URL}/sendMessage", data=data, proxies=proxies, verify=False)

def handle_updates(updates):
    for update in updates:
        message = update.get("message", {})
        text = message.get("text")
        if text != "/start":
            process_telegram_message(message)

def get_updates(last_update_id=None):
    params = {"timeout": 100}
    if last_update_id is not None:
        params["offset"] = last_update_id + 1
    response = requests.get(f"{BASE_URL}/getUpdates", params=params, proxies=proxies, verify=False)
    return response.json().get("result", [])

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if updates:
            handle_updates(updates)
            last_update_id = updates[-1]["update_id"]
        time.sleep(10)

if __name__ == "__main__":
    main()
