# -*- coding: utf-8 -*-

import os
import urllib3
urllib3.disable_warnings()
import requests
from uuid import uuid1
from config import MBlog_Backend_URL, MBlog_TOKEN, Visibility, proxies

headers = {"token": MBlog_TOKEN}
base_url = MBlog_Backend_URL + "/api"

def url_for(endpoint):
    return f"{base_url}/{endpoint}"

def download(url):
    r = requests.get(url, proxies=proxies)
    filename = uuid1().hex + "." + url.split(".")[-1]
    with open(filename, "wb") as f:
        f.write(r.content)
    return filename

def handle_file(file_url):
    file_list = []
    if file_url:
        try:
            filename = download(file_url)
            public_id = upload(filename)
            file_list.append(public_id)
            os.remove(filename)
        except Exception as e:
            print(e)
    return file_list

def get_memo(memo_id):
    url = url_for(f"memo/{memo_id}")
    r = requests.post(url, headers=headers, proxies=proxies, verify=False)
    data = r.json()["data"]
    publicIds = [i["publicId"] for i in data["resources"]]
    return {"visibility": data["visibility"], "publicIds": publicIds, "id": memo_id, 
            "content": data["content"], "priority": 0, "enableComment": data["enableComment"]}

def post_memo(content, file_list=[]):
    r = requests.post(url_for("memo/save"), headers=headers, 
                      json={"content":content, "visibility":Visibility, "publicIds":file_list}, 
                      proxies=proxies, verify=False)
    return r.json()["data"]

def update_memo(memo_id, file_url=""):
    memo = get_memo(memo_id)
    file_list = handle_file(file_url)
    if file_list:
        memo["publicIds"].extend(file_list)
        r = requests.post(url_for("memo/update"), headers=headers, json=memo, proxies=proxies, verify=False)

def upload(file_path):
    with open(file_path, "rb") as f:
        r = requests.post(url_for("resource/upload"), headers=headers, files={"files": f}, proxies=proxies, verify=False)
    return r.json()["data"][0]["publicId"]

def insert(text, file_url=""):
    file_list = handle_file(file_url)
    memo_id = post_memo(text, file_list)
    return memo_id

if __name__ == "__main__":
    public_id = upload("D:/test.png")
    post_memo("测试", [public_id])
