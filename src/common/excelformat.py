"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     excelformat.py
@Author:   shenfan
@Time:     2021/2/7 21:36
"""


class ExcelFormat:
    def __init__(self,rawdata):
        self.rawdata = rawdata

    @property
    def dic_format(self):
        if self.rawdata:
            return eval(self.rawdata)
        else:
            return dict(self.rawdata)


    @property
    def tup_format(self):
        return None

if __name__ == "__main__":
    l = ""
    s = "{\"modelType\":0,\"subProjectId\":2178,\"projectId\": 4089}"
    print(ExcelFormat(l).dic_format,type(ExcelFormat(l).dic_format))
    ExcelFormat(s).dic_format.keys()
    print(ExcelFormat(s).dic_format,type(ExcelFormat(s).dic_format))


