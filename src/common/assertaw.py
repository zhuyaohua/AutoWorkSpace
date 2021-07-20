"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     assertaw.py
@Author:   shenfan
@Time:     2021/2/5 11:11
"""
class ApiAssert:
    def assert_dict(self,expected,result):
        try:
            if isinstance(result,dict):
                for key in expected:
                    if (key in result) & (result[key]==expected[key]):
                        return True
                    else:
                        return False
        except Exception as e:
            print(e)
            raise e