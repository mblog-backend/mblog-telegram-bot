import urllib3
urllib3.disable_warnings()
import requests
import sqlite3
import time
from config import TELEGRAM_TOKEN, MultiUSE, proxies
from telegram_api import process_telegram_message

# 初始化sqlite3数据库
db = sqlite3.connect("data.db")
db.execute('PRAGMA busy_timeout = 5000')
cursor = db.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
if not tables:
    cursor.execute("create table tg_token(int auto_increment primary key,chat_id varchar(32) UNIQUE, mblog_backend varchar(128), mblog_token varchar(512), visit varchar(12), create_time timestamp default CURRENT_TIMESTAMP)")
    db.commit()

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    requests.post(f"{BASE_URL}/sendMessage", data=data, proxies=proxies, verify=False)

def test_connect(mblog_backend, mblog_token):
    url = f"{mblog_backend}/api/user/current"
    headers = {"token": mblog_token}
    try:
        r = requests.post(url, headers=headers, proxies=proxies, verify=False)
    except:
        pass
    else:
        if r.status_code == 200:
            return True

def handle_updates(updates):
    for update in updates:
        message = update.get("message", {})
        chat_id = message["chat"]["id"]
        text = message.get("text") or ""
        if MultiUSE == "True" and text == "/start":
            send_message(chat_id, "欢迎使用MBlog BOT，请输入你的同步可见性、MBlog后端url和开发者token绑定账号，请注意，以英文逗号分隔输入3个参数: \n\nPRIVATE,mblog后端url,mblog开发者token")
        elif MultiUSE == "True" and text.split(',')[0] in ("PRIVATE", "PUBLIC", "PROTECT"):
            visit,backend,token = text.split(",")
            if test_connect(backend, token):
                cursor.execute(f"insert or replace into tg_token(chat_id, mblog_backend, mblog_token, visit) values('{chat_id}', '{backend}', '{token}', '{visit}')")
                db.commit()
                send_message(chat_id, "恭喜！绑定成功，接下来您发送的消息都会同步到您的MBlog。")
            else:
                send_message(chat_id, "绑定失败，请检查后端url或开发者token。")
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
            try:
                handle_updates(updates)
            except Exception as e:
                print(e)
            last_update_id = updates[-1]["update_id"]
        time.sleep(10)

if __name__ == "__main__":
    main()
