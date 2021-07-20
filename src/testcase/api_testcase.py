"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     api_testcase.py
@Author:   shenfan
@Time:     2021/2/17 18:52
"""
from src.common.config import DATA_PATH
from src.common.datareader import ExcelReader
from src.common.interface import Interface
from src.common.excelformat import ExcelFormat
from src.common.assertaw import ApiAssert
import os

class ApiTestCase:
    def __init__(self):
        self.dataexcel = os.path.join(DATA_PATH,"interface_data.xls")
        self.exceldata = ExcelReader(self.dataexcel).data
        self.apiassert = ApiAssert()

    def test_api(self):
        """
        接口自动化测试
        :return:
        """
        resultdatas = []
        for self.data in self.exceldata:
            api = Interface(method=self.data["Method"], url=self.data["URL"], pathparams=self.data["PathParams"], params=self.data["Params"], files=self.data["Files"], data=self.data["Data"]).request()
            self.data["Status"] = api["Status"]
            self.data["Response"] = api["Response"]
            self.data["Elapsed"] = str(api["Elapsed"])
            verify = ExcelFormat(self.data["Verify"]).dic_format
            if self.apiassert.assert_dict(verify,api["Response"]):self.data["Result"]="Pass"
            else:self.data["Response"]="False"
            resultdatas.append(self.data)
        return resultdatas


if __name__ == "__main__":
    print(ApiTestCase().test_api())




