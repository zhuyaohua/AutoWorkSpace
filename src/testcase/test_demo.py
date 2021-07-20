'''
调试脚本
'''
"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     LoginAW.py
@Author:   shenfan
@Time:     2020/8/26 15:33
"""
from src.testcase.case_model import Model
from src.common.log import Logger
from src.common.action import Action
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import requests
import json

logger = Logger(logger_name="TestCase").get_logger()


# class Doctool(Model):
#     def test_login(self):
#         """
#         登录
#         :return:
#         """
#         logger.info(self.test_login.__doc__.split("\n")[1].strip(" "))
#         action = Action(self.driver)
#         self.assertEqual(action.get_text(("xpath", "//div[@class='user-name']/p[1]")),"xxx")
#         action.is_text_in_element(("xpath", "//div[@class='user-name']/p[2]"),"沈番")
#
#     def test_profile(self):
#         """
#         项目首页
#         :return:
#         """
#         logger.info(self.test_profile.__doc__.split("\n")[1].strip(" "))
#         action = Action(self.driver)
#         action.is_element_present(("xpath","//div[@class='project-list-content']"))
#         action.click()
#
#     def test_project(self):
#         """
#         项目切换
#         1、下拉选择项目
#         2、切换项目，验证项目是否切换成功
#         :return:
#         """
#         logger.info(self.test_project.__doc__.split("\n")[1].strip(" "))
#         action = Action(self.driver)
#         action.click(("xpath","//div[@class='cbim-web__nav-pswrap']/div/div/span/span/i[@class='el-select__caret el-input__icon el-icon-arrow-up']"))
#         action.click(("xpath","//li//span[contains(text(),'测试项目-csxm')]"))
#         action.is_text_in_element(("xpath","//span[contains(text(),'当前项目')]/following-sibling::span"),"测试项目-csxm")

class Delivery_GH01(Model):
    def test_selectobject_01(self):
        """
        项目驾驶舱
        1、上传文件
        2、选择模型作为审查对象
        :return:
        """
        ActionChains(self.driver).move_to_element(
            self.driver.find_element_by_xpath("//div[@class='el-tabs__content']/span/div/i")).perform()
        # mouse = self.driver.find_element_by_xpath("//div/span[text()='交付接口自动化-勿动'][1]")
        mouse = self.driver.find_element_by_xpath("//div[@class='cbim-project-search']/div/input")
        mouse.click()
        mouse.send_keys("南京")
        self.driver.find_element_by_xpath("//div[@class='custom-node-item']/div/div/div/div/span[2]").click()
        time.sleep(10)
        # print(mouse.location)
        # ActionChains(self.driver).move_by_offset(mouse.location["x"],mouse.location["y"]).click().perform()
        #
        # print(mouse.id)
        # print(mouse.rect)
        # print(mouse.text)
        # print(mouse.get_attribute("value"))
        # print(mouse.get_attribute("class"))
        # print(mouse.tag_name)
        # print(mouse.location)
