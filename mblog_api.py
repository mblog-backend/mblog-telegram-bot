# -*- coding: utf-8 -*-

import os
import urllib3
urllib3.disable_warnings()
import sqlite3
import requests
from uuid import uuid1
from config import TELEGRAM_TOKEN, MBlog_Backend_URL, MBlog_TOKEN, Visibility, proxies
from telegram_api import send_message

# 初始化sqlite3数据库
db = sqlite3.connect("data.db")
cursor = db.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
if not tables:
    cursor.execute("create table tg_token(int auto_increment primary key,telegram_id varchar(32), mblog_token varchar(512), create_time timestamp default CURRENT_TIMESTAMP)")
    db.commit()


base_url = MBlog_Backend_URL + "/api"

def get_headers(chat_id):
    cursor.execute(f"select mblog_token from tg_token where telegram_id='{chat_id}'")
    mblog_token = cursor.fetchone()
    if mblog_token:
        headers = {"token": mblog_token[0]}
    else:
        headers = {}
    return headers

def url_for(endpoint):
    return f"{base_url}/{endpoint}"

def download(url):
    r = requests.get(url, proxies=proxies)
    filename = uuid1().hex + "." + url.split(".")[-1]
    with open(filename, "wb") as f:
        f.write(r.content)
    return filename

def handle_file(file_url, headers={}):
    file_list = []
    if file_url:
        try:
            filename = download(file_url)
            public_id = upload(filename, headers)
            file_list.append(public_id)
            os.remove(filename)
        except Exception as e:
            print(e)
    return file_list

def get_memo(memo_id, headers={}):
    url = url_for(f"memo/{memo_id}")
    r = requests.post(url, headers=headers, proxies=proxies, verify=False)
    data = r.json()["data"]
    publicIds = [i["publicId"] for i in data["resources"]]
    return {"visibility": data["visibility"], "publicIds": publicIds, "id": memo_id, 
            "content": data["content"], "priority": 0, "enableComment": data["enableComment"]}

def post_memo(content, file_list=[], headers={}):
    r = requests.post(url_for("memo/save"), headers=headers, 
                      json={"content":content, "visibility":Visibility, "publicIds":file_list}, 
                      proxies=proxies, verify=False)
    return r.json()["data"]

def update_memo(memo_id, file_url="", chat_id=""):
    if chat_id:
        headers = get_headers(chat_id)
    else:
        headers = {"token": MBlog_TOKEN}
    if not headers:
        send_message(chat_id, "账号未绑定，请输入/start进行绑定。")
        return
    memo = get_memo(memo_id, headers)
    file_list = handle_file(file_url, headers)
    if file_list:
        memo["publicIds"].extend(file_list)
        r = requests.post(url_for("memo/update"), headers=headers, json=memo, proxies=proxies, verify=False)

def upload(file_path, headers={}):
    with open(file_path, "rb") as f:
        r = requests.post(url_for("resource/upload"), headers=headers, files={"files": f}, proxies=proxies, verify=False)
    return r.json()["data"][0]["publicId"]

def insert(text, file_url="", chat_id=""):
    if chat_id:
        headers = get_headers(chat_id)
    else:
        headers = {"token": MBlog_TOKEN}
    if not headers:
        send_message(chat_id, "账号未绑定，请输入/start进行绑定。")
        return
    file_list = handle_file(file_url, headers)
    memo_id = post_memo(text, file_list, headers)
    return memo_id

if __name__ == "__main__":
    public_id = upload("D:/test.png")
    post_memo("测试", [public_id])
