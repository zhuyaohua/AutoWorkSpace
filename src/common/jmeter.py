"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     jmeter.py
@Author:   shenfan
@Time:     2021/2/13 15:20
"""
import threading
from src.common.config import DATA_PATH
import os
from src.common.datareader import ExcelReader
from src.common.interface import Interface
from datetime import datetime



class Jmeter(threading.Thread):
    def __init__(self, func, args):
        super(Jmeter, self).__init__()
        self.func = func
        self.args = args

    def getresult(self):
        self.res = self.func()
        return self.res


def convert(items, id):
    for key, value in items.items():
        for keys, values in id.items():
            if keys == key:
                items[key] = values
    return items


def main(exceldata):
    # dataexcel = os.path.join(DATA_PATH,"interface_data.xls")
    # exceldata = ExcelReader(dataexcel).data
    apis = []
    for data in exceldata:
        api = Interface(method=data["Method"],host=data["Host"],headers=data["Headers"],url=data["URL"],pathparams=data["PathParams"],params=data["Params"],files=data["Files"],data=data["Data"])
        apis.append((api, data["Code"], data["ThreadNum"], data["Times"]))
    threads = {}
    for func in apis:
        temp= []
        for i in range(0,int(func[2])):
            t = Jmeter(func[0].request,(i,))
            temp.append(t)
        threads[func[1]]=temp
    for threadkey in threads:
        for thread in threads[threadkey]:
            thread.setDaemon(True)
            thread.start()
    threadsresult = []
    for threadkey in threads:
        for thread in threads[threadkey]:
            thread.join(100)
            threadsresult.append((threadkey,thread.getresult()))
    return threadsresult











