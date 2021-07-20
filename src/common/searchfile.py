"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     searchfile.py
@Author:   shenfan
@Time:     2021/2/2 9:08
"""
import os
from src.common.config import REPORT_PATH


def findfile(path=REPORT_PATH):
    abspath = os.path.abspath(path)  # 默认当前目录
    filelist = []
    root = abspath
    for root, dirs, files in os.walk(root):
        for name in files:
            if name.endswith(".html") and name.startswith("DocTool"):
                filelist.append(os.path.join(root, name))
    if len(filelist) != 0:
        return filelist[-1]
    else:
        raise FileNotFoundError('文件不存在！')



if __name__ == '__main__':  # 用于调试
    print(REPORT_PATH)
    print(findfile())





