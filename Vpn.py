# -*- coding:utf-8 -*-
import time
import logger
import logging
from OpenPhone import Open
import os
import re
from IP_Filtering import ip_fiter
class vpn():
    def __init__(self,deviceid,port):
        self.appPackage='it.colucciweb.sstpvpnclient'
        self.appActivity='it.colucciweb.sstpvpnclient.MainActivity'
        #self.appActivity = '.MainActivity'
        self.deviceid=deviceid
        self.port=port
    # 打开VPN
    def newvpn(self,m,t,filtering_mode):
        try:
            self.old_ip = os.popen('adb -s ' + self.deviceid + ' shell curl ip.cip.cc').read().strip('\n')
        except:pass
        os.system('adb -s ' + self.deviceid + ' shell am force-stop com.tencent.mm')
        driver = Open().Phone(self.appPackage, self.appActivity, self.deviceid, self.port)
        driver.implicitly_wait(60)
        while True:
            driver.find_element_by_id('it.colucciweb.sstpvpnclient:id/start_stop').click()  # 开启VPN
            time.sleep(int(t))
            # = driver.find_element_by_id('it.colucciweb.sstpvpnclient:id/details1').get_attribute(("text"))
            #if u"(已连接)" == pd:
            try:
                self.ip = os.popen('adb -s ' + self.deviceid + ' shell curl ip.cip.cc').read().strip('\n')
                if self.old_ip != self.ip:
                    if m == '1':
                        if ip_fiter(self.deviceid, self.ip, filtering_mode) == True:
                            logging.info(self.deviceid + u"-IP地址:%s" % self.ip)
                            return self.ip
                        else:
                            pass
                    if m == '2':
                        return self.ip
                else:
                    logging.info(self.deviceid + u'网络异常 ,请查看手机是否可以正常联网')
            except:
                pass


