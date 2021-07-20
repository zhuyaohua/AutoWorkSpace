"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     report.py
@Author:   shenfan
@Time:     2021/1/29 11:22
"""
import os
import sys
from src.common.config import REPORT_PATH
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from src.common.HTMLTestRunner3 import HTMLTestRunner
import time


class Reportset:
    def __init__(self, filename, title, description):
        """
        设置报告文件保存路径
        :param filename: 测试报告文件名
        :param title: 测试报告主题
        :param description: 测试报告描述
        """

        self.filename = os.path.join(REPORT_PATH, filename) + time.strftime("%Y%m%d%H%M%S ", time.localtime(time.time()))+ ".html"
        self.data = open(self.filename, "wb")
        self.title = title
        self.description = description
        self.runner = HTMLTestRunner(stream=self.data, title=self.title, description=self.description, verbosity=2)


    @property
    def generate_report(self):
        return self.runner





