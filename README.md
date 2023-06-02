# mblog-telegram-bot
这是一个简单的程序，可以将发送给 telegram bot 的消息同步到mblog。

## 准备工作

1. 创建一个 [telegram bot](https://t.me/botfather) 并获取token。

2. 启用mblog开发者token。


## Docker部署

1. 安装Docker

    - ubuntu: `sudo apt install docker`
    - centos: `sudo yum install docker-ce`

2. 运行程序

    ``` bash
    docker run -d \
               --name mblog-telegram-bot \
               --restart unless-stopped \
               -e TELEGRAM_TOKEN="telegram bot token" \
               -e MBlog_Backend_URL="mblog后端url" \
               -e MBlog_Token="mblog开发者token" \
               -e Visibility="mblog发布可见权限，默认仅自己可见，可不配置" \
               -e PROXY_URL="墙内机器运行需要配置telegram代理，墙外无需配置" \
    cooolr/mblog-telegram-bot:latest
    ```

## 常规部署

1. 安装依赖

    ``` bash
    pip install -r requirements.txt
    ```

2. 在 `config.py` 中配置

    - telegram bot token

       `TELEGRAM_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxx"`

    - mblog后端url

       `MBlog_Backend_URL = "http://xxxxxx:xxxx"`

    - mblog开发者token
  
       `MBlog_Token = "xxxxxxxxxxxxxxxxxxxxxxxxx"`

    - mblog发布可见权限，默认`PRIVATE`仅自己可见 (`PUBLIC`所有人可见、`PROTECT`登录用户可见)

       `Visibility = "PRIVATE"`

    - 墙内机器运行需要配置telegram代理，墙外无需配置

      `PROXY_URL = ""`

3. 运行程序

    ``` bash
    python3 main.py
    ```

将 Telegram 机器人添加到聊天中，然后开始发送消息。
