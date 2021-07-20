"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     EmailSet.py
@Author:   shenfan
@Time:     2020/8/27 8:55
"""
import yaml
import time
from xlrd import open_workbook
from xlutils.copy import copy
from xlwt import Workbook,Worksheet
import os


class YamlReader:
    def __init__(self, yamlfile):
        if os.path.exists(yamlfile):
            self.yamlfile = yamlfile
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    @property
    def data(self):
        # 如果第一次调用data，读取yaml文档，否则直接返回之前保存的数据
        if not self._data:
            with open(self.yamlfile, 'rb') as file:
                self._data = list(yaml.safe_load_all(file))
        return self._data













