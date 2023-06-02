import os

# Telegram configuration
TELEGRAM_TOKEN = ""

# mblog backend url
MBlog_Backend_URL = ""

# mblog token
MBlog_Token = ""

# 可见权限
Visibility = "PRIVATE"

# 代理
PROXY_URL = ""

# 从环境变量获取
env = os.environ
if env.get("TELEGRAM_TOKEN"):
    TELEGRAM_TOKEN = env.get("TELEGRAM_TOKEN")
if env.get("PROXY_URL"):
    PROXY_URL = env.get("PROXY_URL")
if env.get("MBlog_Backend_URL"):
    PROXY_URL = env.get("MBlog_Backend_URL")
if env.get("MBlog_Token"):
    PROXY_URL = env.get("MBlog_Token")
if env.get("Visibility"):
    PROXY_URL = env.get("Visibility")

proxies = {"http": PROXY_URL, "https": PROXY_URL}
