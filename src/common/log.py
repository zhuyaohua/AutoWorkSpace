"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     log.py
@Author:   shenfan
@Time:     2021/2/2 9:07
"""
import logging
from logging.handlers import TimedRotatingFileHandler
from src.common.config import LOG_PATH, Config
import os


class Logger(object):
    def __init__(self, logger_name='Autotest'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        self.log_file_name = Config().get('log').get('file_name')
        self.backup_count = Config().get('log').get('backup')

        # 日志输出级别
        self.console_output_level = Config().get('log').get('console_level')
        self.file_output_level = Config().get('log').get('file_level')
        # 日志输出格式
        self.formatter = logging.Formatter(Config().get('log').get('pattern'))

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回"""
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # 每天重新创建一个日志文件，最多保留backup_count份
            file_handler = TimedRotatingFileHandler(filename=os.path.join(LOG_PATH, self.log_file_name),
                                                    when='D',
                                                    interval=1,
                                                    backupCount=self.backup_count,
                                                    delay=True,
                                                    encoding='utf-8'
                                                    )
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger


# logger = Logger().get_logger()







