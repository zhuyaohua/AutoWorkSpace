"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     mutimodels.py
@Author:   shenfan
@Time:     2021/2/24 9:33
"""
from src.common.log import Logger
from selenium import webdriver
from src.common.config import Config,DRIVER_PATH
import os
from selenium.webdriver.chrome.options import Options
import multiprocessing
import time

logger = Logger(logger_name="负载均衡").get_logger()


def browseroptions(browser):
    if browser == "Chrome":
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        chrome_options.add_argument('--start-maximized')  # 指定浏览器分辨率
        chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        # chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        return chrome_options


def graphics_case(xpathname):
    cfg = Config()
    username = cfg.get("env").get("Username")
    entcode = cfg.get("env").get("EntCode")
    passwd = cfg.get("env").get("Passwd")
    url = cfg.get("env").get("URL")
    chrome_options = browseroptions("Chrome")
    driver = webdriver.Chrome(executable_path=os.path.join(DRIVER_PATH, "chromedriver.exe"),options=chrome_options)
    try:
        driver.get(url)
        logger.info("打开URL: %s" % url)
        driver.maximize_window()
        logger.info("全屏当前窗口")
        driver.implicitly_wait(5)
        logger.info("设置5秒隐式等待时间")
        driver.find_element_by_xpath("/html/body/div[2]/ul/li[2]").click()
        driver.find_element_by_xpath("//div/input[@name='username']").send_keys( username)
        driver.find_element_by_xpath("//div/input[@name='password']").send_keys( passwd)
        driver.find_element_by_xpath("//div[contains(text(),'登录')]").click()
        driver.refresh()
    except Exception as e:
        logger.info(str(e))

    driver.find_element_by_id("tab-0").click()
    driver.find_element_by_xpath("//div[@class='cbim-web__nav-pswrap']/div/div/span/span/i").click()
    driver.find_element_by_xpath("//span[text()='交付接口自动化-勿动']").click()
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div/div[1]/div/div/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div/span/span/i").click()
    time.sleep(3)
    driver.find_element_by_xpath("//span[text()='图形实例-%s']"%xpathname).click()
    driver.find_element_by_xpath("//div/div/div[2]/a[@class='upload-btn' and text()='上传模型']").click()
    time.sleep(30)
    uploads = driver.find_element("xpath","//div/div/div[3]/div/div[2]/div[1]/div/input")
    uploads.send_keys(r"C:\Users\SHENFAN\Desktop\中设数字\CBIM-中设数字-模板\交付模型\测试模型\农科院合并-20210225.cim")
    time.sleep(300)
    driver.find_element_by_xpath("//div/div/div[3]/div/div[3]/span/button[2]").click()
    num = len(driver.find_elements("xpath","//span[@class='el-checkbox__inner']"))
    xpath = "//div/div/div[1]/div[3]/table/tbody/tr[%s]/td[4]/div/label/span[1]/span"%num
    driver.find_element_by_xpath(xpath).click()
    time.sleep(2)
    driver.quit()


def clearmodels(xpathname):
    cfg = Config()
    username = cfg.get("env").get("Username")
    entcode = cfg.get("env").get("EntCode")
    passwd = cfg.get("env").get("Passwd")
    url = cfg.get("env").get("URL")
    chrome_options = browseroptions("Chrome")
    driver = webdriver.Chrome(executable_path=os.path.join(DRIVER_PATH, "chromedriver.exe"),options=chrome_options)
    try:
        driver.get(url)
        logger.info("打开URL: %s" % url)
        driver.maximize_window()
        logger.info("全屏当前窗口")
        driver.implicitly_wait(5)
        logger.info("设置5秒隐式等待时间")
        driver.find_element_by_xpath("/html/body/div[2]/ul/li[2]").click()
        driver.find_element_by_xpath("//div/input[@name='username']").send_keys( username)
        driver.find_element_by_xpath("//div/input[@name='password']").send_keys( passwd)
        driver.find_element_by_xpath("//div[contains(text(),'登录')]").click()
        time.sleep(2)
    except Exception as e:
        logger.info(str(e))
    time.sleep(3)
    driver.find_element_by_id("tab-0").click()
    driver.find_element_by_xpath("//div[@class='cbim-web__nav-pswrap']/div/div/span/span/i").click()
    driver.find_element_by_xpath("//span[text()='交付接口自动化-勿动']").click()
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div/div[1]/div/div/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div/span/span/i").click()
    time.sleep(3)
    element = driver.find_element_by_xpath("//span[text()='xxx%s']"%xpathname)
    print("线程%s"%xpathname,element.text)
    element.click()
    time.sleep(2)
    delelementnum = len(driver.find_elements_by_xpath("//span[text()='模型管理']/../../following-sibling::div/div/div/div[1]/div[3]/table/tbody/tr/td/div/button/span[text()='删除']"))
    for i in range(delelementnum):
        time.sleep(2)
        delelements = driver.find_elements_by_xpath("//span[text()='模型管理']/../../following-sibling::div/div/div/div[1]/div[3]/table/tbody/tr/td/div/button/span[text()='删除']")
        if delelements:
            delelements[0].click()
            driver.find_element_by_xpath("//span[contains(text(),'确定')]").click()
            time.sleep(2)
    driver.quit()


def synch(func,threadnum):
    for i in range(threadnum):
        p = multiprocessing.Process(target=func,args=(i,))
        p.start()
    p.join()
    p.run()


if __name__ == "__main__":
    # synch(clearmodels,31)
    # graphics_case(1)
    # clearmodels("x")
    while True:
        graphics_case(1)







