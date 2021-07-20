"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     case_model.py
@Author:   shenfan
@Time:     2021/1/29 13:10
"""
import unittest
from src.common.config import Config
from src.common.browserdriver import BrowserDriver
from src.common.log import Logger

logger = Logger(logger_name="setUp").get_logger()


class Model(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cfg = Config()
        cls.username = cfg.get("env").get("Username")
        # cls.entcode = cfg.get("env").get("EntCode")
        cls.passwd = cfg.get("env").get("Passwd")
        try:
            driver = BrowserDriver(cls)
            cls.driver = driver.open_browser(cls)
            cls.driver.find_element_by_xpath("/html/body/div[2]/ul/li[2]").click()
            cls.driver.find_element_by_xpath("//div/input[@name='username']").send_keys(cls.username)
            cls.driver.find_element_by_xpath("//div/input[@name='password']").send_keys(cls.passwd)
            cls.driver.find_element_by_xpath("//div[contains(text(),'登录')]").click()
        except Exception as e:
            logger.info(str(e))
        return cls.driver.get_cookies()


    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass


if __name__ == "__main__":
    print(Config().get("env").get("URL"))




