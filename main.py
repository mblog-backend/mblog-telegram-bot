import urllib3
urllib3.disable_warnings()
import requests
import sqlite3
import time
from config import TELEGRAM_TOKEN, MultiUSE, proxies
from telegram_api import process_telegram_message

# 初始化sqlite3数据库
db = sqlite3.connect("data.db")
cursor = db.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
if not tables:
    cursor.execute("create table tg_token(int auto_increment primary key,telegram_id varchar(32), mblog_token varchar(512), create_time timestamp default CURRENT_TIMESTAMP)")
    db.commit()

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    requests.post(f"{BASE_URL}/sendMessage", data=data, proxies=proxies, verify=False)

def handle_updates(updates):
    for update in updates:
        message = update.get("message", {})
        text = message.get("text")
        if MultiUSE == "True" and text == "/start":
            chat_id = message["chat"]["id"]
            send_message(chat_id, "欢迎使用MBlog BOT，请输入你的MBlog开发者token绑定账号，请注意，以以下格式输入: \n`mblog-token=你的token`")
        elif MultiUSE == "True" and text[:12] == "mblog-token=":
            chat_id = message["chat"]["id"]
            telegram_id = message["from"]["id"]
            mblog_token = text.split("=")[-1]
            cursor.execute(f"insert into tg_token(telegram_id, mblog_token) values('{telegram_id}', '{mblog_token}')")
            db.commit()
            send_message(chat_id, "恭喜！绑定成功，接下来您发送的消息都会同步到您的MBlog。")
        elif MultiUSE == "True":
            process_telegram_message(message, chat_id)
        else:
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
