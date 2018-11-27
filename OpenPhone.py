# -*- coding:utf-8 -*-
import re
from appium import webdriver
import requests
import os
import re
import logging
import logger
import time
class Open():
    try:
        def Phone(self ,appPackage,appActivity,deviceid,port):
            desired_caps = {}
            desired_caps['platformName'] = 'Android'  # 设备系统
            desired_caps['automationName'] = 'UiAutomator2'
            #desired_caps['platformVersion'] = '8.0.0'  # 设备系统版本
            desired_caps['platformVersion'] = os.popen('adb -s %s shell getprop ro.build.version.release' % deviceid).readlines()[0].strip('\n')  # 设备系统版本
            desired_caps['deviceName'] = deviceid # 设备名称
            desired_caps['appPackage'] = appPackage
            desired_caps['appActivity'] = appActivity
            desired_caps['udid'] = deviceid
            desired_caps['unicodeKeyboard'] = "True"
            desired_caps['resetKeyboard'] = "True"
            try:
                driver = webdriver.Remote('http://localhost:'+port+'/wd/hub',desired_caps)
                return driver
            except:
                logging.info('%s-appium服务端未开启,请检查'%deviceid)
    except :
        pass

if __name__ == '__main__':
    decice='53476787'
    while True:
        if  os.system('adb -s %s shell cd /sdcard'%decice) != 0:
            logging.info('1')
            #raise Exception, "%s-未连接到手机"%decice
        else:
            pass

    #if decice in a:
    #    driver = Open().Phone('com.dobe.sandbox', '.home.Main2Activity', decice, '4713')
    #    driver.implicitly_wait(50)
    #    driver.find_element_by_id('com.dobe.sandbox:id/appIcon').click()
    #    #driver.find_element_by_name('微信').click()














