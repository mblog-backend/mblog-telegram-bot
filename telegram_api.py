import os
import time
import urllib3
urllib3.disable_warnings()
import requests
from uuid import uuid1
from mblog_api import insert, update_memo
from config import TELEGRAM_TOKEN, proxies

os.chdir(os.path.dirname(os.path.abspath(__file__)))
memo_timestamp_dict = {}

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    requests.post(f"{BASE_URL}/sendMessage", data=data, proxies=proxies, verify=False)

def get_file_url(file_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getFile?file_id={file_id}"
    r = requests.get(url, proxies=proxies)
    file_path = r.json()["result"]["file_path"]
    return f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"

def process_link_text(message):
    text = message.get('text', '') or message.get('caption', '')
    entities = message.get('entities', []) or message.get("caption_entities", [])
    entities.sort(key=lambda x: x['offset'], reverse=True)  # sort entities from right to left

    for entity in entities:
        if entity.get('type') == 'text_link':
            offset = entity.get('offset')
            length = entity.get('length')
            url = entity.get('url')
            link_text = text[offset:offset+length]
            markdown_link = f'[{link_text}]({url})'
            text = text[:offset] + markdown_link + text[offset+length:]
    return text

def process_telegram_message(message, chat_id=""):
    global memo_timestamp_dict
    print(message)
    memo_timestamp_dict = {k: v for k, v in memo_timestamp_dict.items() if time.time() - k <= 300}
    text = process_link_text(message)
    file_url = ""
    file_types = ["document", "photo", "video_note", "animation"]
    for f_type in file_types:
        if message.get(f_type):
            file_id = message[f_type]["file_id"] if f_type != "photo" else message[f_type][-1]["file_id"]
            file_url = get_file_url(file_id)
            break

    if memo_timestamp_dict.get(message["date"]):
        update_memo(memo_timestamp_dict[message["date"]], file_url, chat_id)
    else:
        memo_id = insert(text, file_url, chat_id)
        if memo_id:
            memo_timestamp_dict[message["date"]] = memo_id
