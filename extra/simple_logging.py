# -*- coding: utf-8 -*-

import logging

def initialization_logging():
    # 设置root_logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    # 创建一个handler，用于写入日志文件
    file_handler = logging.FileHandler('main.log')
    file_handler.setLevel(logging.DEBUG)
    # 再创建一个handler，用于输出到控制台
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    # 给logger添加handler
    # root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)
    return root_logger

logger = initialization_logging()