"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     config.py
@Author:   shenfan
@Time:     2021/2/2 9:10
"""
import os
from src.common.configreader import YamlReader

# 通过当前文件的绝对路径，其父级目录一定是框架的base目录，然后确定各层的绝对路径。如果你的结构不同，可自行修改。
BASE_PATH = os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")), ".."))
CONFIG_FILE = os.path.join(BASE_PATH, 'configure', 'config.yml')
ENV_FILE = os.path.join(BASE_PATH, 'configure', 'envinfo.yaml')
DATA_PATH = os.path.join(BASE_PATH, 'data')
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')
TESTCASE_PATH = os.path.join(BASE_PATH,"src","testcase")
SCREEN_PATH = os.path.join(BASE_PATH,"screenshot")



class Config:
    def __init__(self, config=CONFIG_FILE):
        self.config = YamlReader(config).data

    def get(self, element, index=0):
        """
        yaml是可以通过'---'分节的。用YamlReader读取返回的是一个list，第一项是默认的节，如果有多个节，可以传入index来获取。
        这样我们其实可以把框架相关的配置放在默认节，其他的关于项目的配置放在其他节中。可以在框架中实现多个项目的测试。
        """
        return self.config[index].get(element)


if __name__ == '__main__': #用于调试
    print(ENV_FILE)
    print(Config(ENV_FILE).get("Dev"))
    print(os.path.join(DRIVER_PATH,"chromedriver.exe"))











