import logging

# 创建并配置日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 创建日志处理程序
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 创建日志格式器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 将日志格式器添加到处理程序
console_handler.setFormatter(formatter)

# 将处理程序添加到日志记录器
logger.addHandler(console_handler)

def log(func):
    def wraper(*args, **kw):
        logger.info(f"call function -> {func.__name__}")
        try:
            return func(*args, **kw)
        except Exception as e:
            logger.error(e)
    return wraper

# 示例日志记录
if __name__ == "__main__":
    logger.debug('这是一个调试信息')
    logger.info('这是一个信息')
    logger.warning('这是一个警告')
    logger.error('这是一个错误')
    logger.critical('这是一个严重错误')

