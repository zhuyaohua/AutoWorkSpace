"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     apireport.py
@Author:   shenfan
@Time:     2021/2/19 9:11
"""
from src.common.jmeter import main,convert
from src.common.datareader import ExcelReader,ExcelWrite
from src.common.config import DATA_PATH
from src.common.assertaw import ApiAssert
import os
import time


def reportprocessing():
    dataexcel = os.path.join(DATA_PATH,"interface_data.xls")
    exceldata = ExcelReader(dataexcel,sheet=3).data
    threads_result = main(exceldata)
    finalldata = []
    for data in exceldata:
        for result in threads_result:
            if data["Code"] == result[0]:
                flag = ApiAssert().assert_dict(eval(data["Verify"]),result[1]["Response"])
                if flag: result[1]["Result"]="Pass"
                else:result[1]["Result"]="False"
    # for result in threads_result:
    #     print(result)
    thread_elapsed_result = []
    for data in exceldata:
        elapsed = 0.00
        SuceesTimes = 0.00
        FailTimes = 0.00
        elapsed_result={"SuceesTimes":0.00,"FailTimes":0.00}
        for result in threads_result:
            if data["Code"] == result[0]:
                elapsed_result["Code"] = data["Code"]
                if result[1]["Result"] == "Pass":
                    elapsed += result[1]["Elapsed"]
                    SuceesTimes += 1.00
                    elapsed_result["Elapsed"] = elapsed
                    elapsed_result["SuceesTimes"] = SuceesTimes
                if result[1]["Result"] == "False":
                    FailTimes += 1.00
                    elapsed_result["FailTimes"] = FailTimes
        thread_elapsed_result.append(elapsed_result)
    for item in thread_elapsed_result:
        if item["FailTimes"]:
            for result in threads_result:
                if item["Code"] == result[0] and result[1]["Result"]=="False":
                    item["Status"] = result[1]["Status"]
                    item["Result"] = result[1]["Result"]
                    item["Response"] = result[1]["Response"]
                    break
        else:
            for result in threads_result:
                if item["Code"] == result[0] and result[1]["Result"]=="Pass":
                    item["Status"] = result[1]["Status"]
                    item["Result"] = result[1]["Result"]
                    item["Response"] = result[1]["Response"]
                    break
    for item in thread_elapsed_result:
        if item["SuceesTimes"]:
            item["Elapsed"] = float(item["Elapsed"]/item["SuceesTimes"])
    for data in exceldata:
        for itemdata in thread_elapsed_result:
            if data["Code"]==itemdata["Code"]:
                finalldata.append(convert(data,itemdata))
    e = ExcelWrite(finalldata)
    e.write()



if __name__ == "__main__":
    reportprocessing()

