"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     interface.py
@Author:   shenfan
@Time:     2021/2/7 13:47
"""
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import hashlib
import time
from src.common.config import Config, ENV_FILE, DATA_PATH
from src.common.datareader import ExcelReader, ExcelWrite
import os
import json
from src.common.excelformat import ExcelFormat
from src.common.assertaw import ApiAssert
import filetype


def translator():
    pass


class _Ticker:
    def __init__(self, env, username, password, entcode):
        self.env = env
        self.username = username
        self.entcode = entcode
        self.password = password
        self.__uri = Config(ENV_FILE).get(env).get("ticket").get("uri")
        self.__appkey = Config(ENV_FILE).get(env).get("ticket").get("appkey")
        self.__appid = Config(ENV_FILE).get(env).get("ticket").get("appid")
        self.__ts = str(int(time.time() * 1000))
        sha1 = hashlib.sha1((self.__appkey + "," + self.__uri + "," + self.__ts).replace("-", "").encode("utf-8"))
        self.__sign = sha1.hexdigest().lower()
        self.__headers = {
            "Content-Type": "application/json",
            "appid": self.__appid,
            "sign": self.__sign,
            "ts": self.__ts,
        }
        self.__params = {
            "userName": self.username,
            "password": self.password,
            "code": self.entcode
        }
        self.__url = Config(ENV_FILE).get(env).get("environ").get("cas") + self.__uri

        try:
            reponse_tickct = requests.request(method="post", url=self.__url, headers=self.__headers,
                                              data=json.dumps(self.__params), verify=False)
            self.ticket = reponse_tickct.json().get("data").get("ticket")
            self.entid = reponse_tickct.json().get("data").get("entId")
            self.userid = reponse_tickct.json().get("data").get("userId")
            print("ticket", self.ticket)
        except:
            print("用户账号异常")
            pass

    def reticket(self):
        return self.ticket
tgt =  _Ticker("Cdev","shenf@cadg.cn","s123456","delivery").reticket()
cookie = {"delivery.tk": tgt,
          "tool.tk": tgt}
class Interface:
    def __init__(self, method, host, url, headers, pathparams, params, files, data):
        self.method = method
        self.url = url
        with open(os.path.join(DATA_PATH, "params.json"), "r") as fdata:
            self.setparams = json.loads(fdata.read())
        self.pathparams = ExcelFormat(pathparams).dic_format
        for key in self.pathparams:
            if str(self.pathparams[key])[1:] in self.setparams.keys():
                self.pathparams[key] = self.setparams[self.pathparams[key][1:]]
        self.params = ExcelFormat(params).dic_format
        for key in self.params:
            if str(self.params[key])[1:] in self.setparams.keys():
                self.params[key] = self.setparams[self.params[key][1:]]
        if files:
            files = eval(files)
            # print(files["filepath"], filetype.guess(files["filepath"]).extension)
            self.files = {
                files["filename"]: open(files["filepath"], "rb")
            }
        else:
            self.files = files
        self.data = ExcelFormat(data).dic_format
        for key in self.data:
            if str(self.data[key])[1:] in self.setparams.keys():
                self.data[key] = self.setparams[self.data[key][1:]]
            if key == "path":
                with open(self.data["path"],"r",encoding="utf-8") as rawdata:
                    self.data = json.dumps(json.loads(rawdata.read()))
        if host:
            self.host = host
        else:
            self.host = Config(config=ENV_FILE).get("Dev").get("environ").get("uri_delivery")
        self.cookies = cookie
        if headers:
            self.headers = ExcelFormat(headers).dic_format
            self.headers["env"] = "cdev"
        else:
            self.headers = {"env": "cdev"}
        self.url = self.host + self.url
        self.finallresult = []

    def request(self):
        self.result = {}
        if self.pathparams:
            if isinstance(self.pathparams, dict):
                self.url = self.url.format(**self.pathparams)
            elif isinstance(self.pathparams, list):
                self.url = self.url.format_map(dict(self.pathparams))
            else:
                raise TypeError
        response = requests.request(method=self.method, url=self.url, headers=self.headers, params=self.params,
                                    data=self.data, files=self.files, cookies=self.cookies, verify=False)
        if response.status_code == 200:
            self.result["Status"] = response.status_code
            self.result["Elapsed"] = response.elapsed.total_seconds()
            self.result["Response"] = response.json()
        else:
            self.result["Status"] = response.status_code
            self.result["Elapsed"] = ""
            self.result["Response"] = response.text
        if self.setparams:
            for key in self.setparams:
                if self.setparams[key][1:] in response.json()["result"][0].keys():
                    self.setparams[key] = response.json()["result"][0][self.setparams[key][1:]]
            with open(os.path.join(DATA_PATH, "params.json"), "w+") as fdata:
                fdata.write(json.dumps(self.setparams, indent=4, ensure_ascii=False))
        with open(os.path.join(DATA_PATH, "result.json"), "w+",encoding="utf-8") as resultdata:
            resultdata.write(json.dumps(response.json(), indent=4, ensure_ascii=False))
        return self.result


if __name__ == "__main__":
    # def convert(items, ID):
    #     for key, value in items.items():
    #         for keys, values in ID.items():
    #             if keys == key:
    #                 items[key] = values
    #     return items
    # basepath = os.path.dirname(os.path.dirname(os.path.abspath(".")))
    # dataexcel = os.path.join(basepath,"data","interface_data.xls")
    # exceldata = ExcelReader(dataexcel).data
    # finalldata = []
    # for data in exceldata:
    #     api = Interface(method=data["Method"],url=data["URL"],pathparams=data["PathParams"],params=data["Params"],files=data["Files"],data=data["Data"])
    #     tempresult = api.request()
    # #     if ApiAssert().assert_dict(eval(data["Verify"]),tempresult["Response"]):data["Result"] = "Pass"
    # #     else:data["Result"] = "False"
    # #     finalldata.append(convert(data,tempresult))
    # #
    # # print(finalldata)
    # # e = ExcelWrite(finalldata)
    # # e.write()
    _Ticker("Cdev", "shenf@cadg.cn", "s123456","delivery")

