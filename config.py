import os

# Telegram configuration
#TELEGRAM_TOKEN = "6066281147:AAGGG9_kRySSuPYVLA5X1Q93Jv4SVYwitxM"
TELEGRAM_TOKEN = ""

# mblog backend url
MBlog_Backend_URL = ""

# mblog token
MBlog_TOKEN = ""

# 可见权限
Visibility = "PRIVATE"

# 代理
PROXY_URL = ""

# 多用户使用
MultiUSE = ""

# 从环境变量获取
env = os.environ
if env.get("TELEGRAM_TOKEN"):
    TELEGRAM_TOKEN = env.get("TELEGRAM_TOKEN")
if env.get("PROXY_URL"):
    PROXY_URL = env.get("PROXY_URL")
if env.get("MBlog_Backend_URL"):
    MBlog_Backend_URL = env.get("MBlog_Backend_URL")
if env.get("MBlog_TOKEN"):
    MBlog_TOKEN = env.get("MBlog_TOKEN")
if env.get("Visibility"):
    Visibility = env.get("Visibility")
if env.get("MultiUSE"):
    MultiUSE = env.get("MultiUSE")
 
proxies = {"http": PROXY_URL, "https": PROXY_URL}
