"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     run.py
@Author:   shenfan
@Time:     2021/1/29 10:38
"""
import unittest
import os
from src.common.report import Reportset
from src.common.config import TESTCASE_PATH,REPORT_PATH
from src.common.emailset import EmailSet
from src.common.datareader import ExcelWrite
from src.testcase.api_testcase import ApiTestCase


def createsuite():
    testsuite = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(start_dir=TESTCASE_PATH,pattern="test*.py")

    for testcase in discover:
        testsuite.addTests(testcase)

    return testsuite


if __name__ == "__main__":
    testsuite = createsuite()
    report = Reportset(filename="DocTool-Test-", title=u"混合端工具测试报告", description=u"用例测试情况")
    reportinfo = report.generate_report.run(testsuite)
    # email = EmailSet()
    # email.attach_file(report.filename)
    # email.send()
    # excel = os.path.join(REPORT_PATH, "report.xlsx")
    # streamdata = ApiTestCase().test_api()
    # ExcelWrite(excel, streamdata)








