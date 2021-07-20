"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     browserdriver.py
@Author:   shenfan
@Time:     2021/1/29 13:47
"""
from selenium import webdriver
from src.common.log import Logger
from selenium.webdriver.chrome.options import Options
from src.common.config import Config,DRIVER_PATH
import os

logger = Logger(logger_name="BrowserDriver").get_logger()


class BrowserDriver(object):
    path = DRIVER_PATH

    def __init__(self,driver):
        self.driver = driver
        self.config = Config()

    def open_browser(self,driver):
        browser = self.config.get("browser").get("BrowserName")
        logger.info("浏览器:%s" % browser)
        url = self.config.get("env").get("URL")
        logger.info("访问:%s" % url)
        if browser == "Chrome":
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
            chrome_options.add_argument('--start-maximized')  # 指定浏览器分辨率
            chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
            chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
            # chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
            # chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('lang=zh_CN.UTF-8')
            driver = webdriver.Chrome(executable_path=os.path.join(DRIVER_PATH, "chromedriver.exe"), options=chrome_options)
            logger.info("启动谷歌浏览器")
        elif browser == "IE":
            driver = webdriver.Ie(os.path.join(DRIVER_PATH, "xxxx.exe"))
            logger.info("启动IE浏览器")
        elif browser == "Firefox":
            driver = webdriver.Firefox(os.path.join(DRIVER_PATH, "xxxx.exe"))
            logger.info("启动FireFox浏览器")

        driver.get(url)
        logger.info("打开URL: %s" % url)
        driver.maximize_window()
        logger.info("全屏当前窗口")
        driver.implicitly_wait(5)
        logger.info("设置5秒隐式等待时间")
        return driver

    def quit_browser(self):
        logger.info("关闭浏览器")
        self.driver.quit()






