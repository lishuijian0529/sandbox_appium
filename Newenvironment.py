# -*- coding: utf-8 -*-
import os
import re
from File import file
from appium.webdriver.common.touch_action import TouchAction
import datetime
from OpenPhone import Open
from PhoneNumber import PhoneNumber
from Analysis import analysis
from SubmissionOrder import submissionorder
import logging
import TokenYZ
import random
import duoduo_api
from Token import token
from weiba_api import WB
import time
import json
import base64
import requests
import zipfile
import traceback
from wjvpn import wj
import Pack
import shutil
class newenvironment():
    def __init__(self, uid, password, pid, deviceid, port, o_username, o_password, wxmm, phmode, wxmc, phonenumber, gj_mode, tm=None, cooperator=None, country=None,gj=None,qh=None,switchingmode=None,filtering_mode=None,t=None,ip=None):
        self.uid = uid
        self.cooperator = cooperator
        self.password = password
        self.pid = pid
        self.deviceid = deviceid
        self.port = port
        self.o_username = o_username
        self.o_password = o_password
        self.wxmm = wxmm
        self.phmode = phmode
        self.ph = PhoneNumber(self.uid, self.password, self.pid, self.deviceid, phmode)
        self.wxmc = wxmc
        self.gj_mode = gj_mode
        self.phonenumber = phonenumber
        self.tm = tm
        self.country = country
        self.gj = gj
        self.qh = qh
        self.w = WB(deviceid)
        self.wj = wj(deviceid, port)
        self.element_json = json.loads(file.read_all('6.7.3.json'))
        self.switchingmode =switchingmode
        self.filtering_mode = filtering_mode
        self.t = t
        self.ip = ip
    #微霸新机
    def wb_new(self):
        #api调用一键新机
        status = self.w.newDevice()
        if status == True:
            logging.info(self.deviceid+u'-一键新机成功')
            logging.info(self.deviceid + u'-准备打开WX')
            self.driver = Open().Phone('com.tencent.mm','.ui.LauncherUI', self.deviceid, self.port)
            self.driver.implicitly_wait(180)
            size = self.driver.get_window_size()
            self.wb = int(size.values()[0]) / 1080
            self.hb = int(size.values()[1]) / 1920

    #多多新机
    def dd_new(self):
        time.sleep(2)
        self.device_token = duoduo_api.newPhone(self.deviceid)
        logging.info(self.deviceid+'-token:%s'%self.device_token)
        time.sleep(2)
        logging.info(self.deviceid + u'-一键新建成功')
        logging.info(self.deviceid + u'-启动WX')
        self.driver = Open().Phone('com.tencent.mm', '.ui.LauncherUI', self.deviceid, self.port)
        self.driver.implicitly_wait(180)
        size = self.driver.get_window_size()

    #沙盒新机
    def sand_box(self):
        os.popen('adb -s %s shell rm -rf /sdcard/boxbackup' % self.deviceid)
        with open('沙盒账密配置.json'.decode('utf-8'), 'r') as f:
            a = json.loads(f.read())
        for i in a:
            if self.deviceid == i['deviceid']:
                username = i['username']
                password = i['password']
        os.popen('adb -s %s shell am force-stop com.dobe.sandbox' % self.deviceid)
        self.driver = Open().Phone('com.dobe.sandbox', '.home.Main2Activity', self.deviceid, self.port)
        self.driver.implicitly_wait(50)
        size = self.driver.get_window_size()
        self.wb = int(size.values()[0]) / 1080
        self.hb = int(size.values()[1]) / 1920
        self.driver.find_element_by_id('com.dobe.sandbox:id/download_icon').click()
        wz = self.driver.find_element_by_id('com.dobe.sandbox:id/textView').get_attribute(('text'))
        while True:
            if wz.encode('utf-8') == '尚未登陆,点击登陆':
                self.driver.find_element_by_name('尚未登陆,点击登陆').click()
                self.driver.find_element_by_id('com.dobe.sandbox:id/editText').send_keys(username)
                self.driver.find_element_by_id('com.dobe.sandbox:id/editText2').send_keys(password)
                self.driver.keyevent('66')
                time.sleep(1)
                self.driver.find_element_by_name('点击登陆').click()
                if self.driver.find_elements_by_id('com.dobe.sandbox:id/download_icon') != []:
                    break
            else:
                self.driver.keyevent('4')
                break
        self.driver.find_element_by_id('com.dobe.sandbox:id/context_menu').click()
        self.driver.find_element_by_name('清除APP数据').click()
        self.driver.find_element_by_name('确认删除').click()
        time.sleep(5)
        self.driver.find_element_by_id('com.dobe.sandbox:id/download_device').click()
        self.driver.find_element_by_name('修改设备').click()
        self.driver.find_element_by_name('修改机型').click()
        b = 0
        self.driver.implicitly_wait(2)
        while True:
            if self.driver.find_elements_by_class_name('android.widget.TextView') != []:
                list = self.driver.find_elements_by_class_name('android.widget.TextView')
                if list.__len__() > 5:
                    self.IMEI = re.findall('IMEI: (.*)', list[2].get_attribute(("text")))[0]
                    logging.info('%s-IMEI:%s' % (self.deviceid,self.IMEI))
                    self.MAC = re.findall('MAC: (.*)', list[5].get_attribute(("text")))[0]
                    logging.info('%s-MAC:%s' % (self.deviceid, self.MAC))
                    self.Brand = re.findall('BRAND: (.*)', list[6].get_attribute(("text")))[0]
                    logging.info('%s-BRAND:%s' % (self.deviceid, self.Brand))
                    self.driver.keyevent(4)
                    time.sleep(1)
                    self.driver.keyevent(4)
                    time.sleep(2)
                    self.driver.find_element_by_id('com.dobe.sandbox:id/appIcon').click()
                    break
                else:
                    if 30 == b:
                        self.driver.quit()
                        break
                    else:
                        b = b + 1
                        time.sleep(2)
    #国内注册
    def register(self):
        self.driver.implicitly_wait(60)
        self.driver.find_element_by_id(self.element_json[u'首页注册ID']).click()
        time.sleep(1)
        self.driver.implicitly_wait(5)
        logging.info(self.deviceid + u'-点击注册')
    #国外输入账号信息

    def Judgment_Devices(self):
        while True:
            if os.system('adb -s %s shell cd /sdcard' % self.deviceid) != 0:
                logging.info(u'%s未检测到手机连接'%self.deviceid)
                time.sleep(5)
            else:
                break

    #国内输入账号信息
    def input_text(self):
        self.Judgment_Devices()
        # for i in  list(self.wxmc):
        #     time.sleep(0.3)
        #     os.system('adb -s %s shell input text %s'%(self.deviceid,i))
        self.driver.find_elements_by_id(self.element_json[u'输入框ID'])[0].send_keys(self.wxmc)
        logging.info(self.deviceid + u'-输入昵称')
        self.driver.find_elements_by_id(self.element_json[u'输入框ID'])[1].clear()
        self.Judgment_Devices()
        logging.info(self.deviceid + u'-清空手机号码')
        #os.system('adb -s %s shell input text %s' % (self.deviceid, self.phonenumber[0]))
        for i in  list(self.phonenumber[0]):
            time.sleep(0.3)
            os.system('adb -s %s shell input text %s'%(self.deviceid,i))
        logging.info(self.deviceid + u'-输入手机号码:' + self.phonenumber[0])
        time.sleep(random.randint(1, 3))
        self.Judgment_Devices()
        self.driver.find_elements_by_id(self.element_json[u'输入框ID'])[2].click()
        for i in  list(self.wxmm):
            time.sleep(0.3)
            os.system('adb -s %s shell input text %s'%(self.deviceid,i))
        logging.info(self.deviceid + u'-输入密码:' + self.wxmm)
        self.driver.implicitly_wait(180)
        time.sleep(random.randint(1, 3))
        self.Judgment_Devices()
        self.driver.find_element_by_id(self.element_json[u'手机号注册页面注册按钮ID']).click()
        logging.info(self.deviceid + u'-点击注册')
        self.driver.implicitly_wait(1)
        while True:
            self.Judgment_Devices()
            if self.driver.find_elements_by_class_name(self.element_json['CheckBox']) != []:
                self.driver.find_elements_by_class_name(self.element_json['CheckBox'])[0].click()
                logging.info(self.deviceid + u'-同意协议')
                os.popen('adb -s %s shell input tap 567 1789'%self.deviceid)
                time.sleep(5)
                break
            self.Judgment_Devices()
            if self.driver.find_elements_by_id(self.element_json[u'手机号注册页面注册按钮ID']) != []:
                self.driver.find_element_by_id(self.element_json[u'手机号注册页面注册按钮ID']).click()
            self.Judgment_Devices()
            if self.driver.find_elements_by_name('网页无法打开') != []:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                self.driver.quit()
                break
            self.Judgment_Devices()
            if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("网页无法打开")') != []:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                self.driver.quit()
                break
            self.Judgment_Devices()
            if self.driver.find_elements_by_name('找不到网页') != []:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                self.driver.quit()
                break
        time.sleep(4)
        while True:
            self.Judgment_Devices()
            if self.driver.find_elements_by_class_name(self.element_json['CheckBox']) != []:
                self.driver.find_elements_by_class_name(self.element_json['CheckBox'])[0].click()
                logging.info(self.deviceid + u'-同意协议')
                os.popen('adb -s %s shell input tap 567 1789' % self.deviceid)
            if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID']) != []:
                self.driver.find_element_by_id(self.element_json[u'错误弹窗确定ID']).click()
            if self.driver.find_elements_by_name('微信安全')!=[]:
                logging.info(self.deviceid + u'-进入滑图页面')
                break
            if self.driver.find_elements_by_name('网页无法打开') != []:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                self.driver.quit()
                break
            if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("网页无法打开")') != []:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                self.driver.quit()
                break
            if self.driver.find_elements_by_name('找不到网页') != []:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                self.driver.quit()
                break
            os.popen('adb -s %s shell input tap 500 900' % self.deviceid)
            os.popen('adb -s %s shell input tap 460 1096' % self.deviceid)
        time.sleep(5)

    # 小蚂蚁
    def xmy(self):
        os.system('adb -s %s shell input tap 1056 573' % self.deviceid)
        time.sleep(1)
        os.system('adb -s %s shell input tap 580 630' % self.deviceid)

    #滑图错误
    def error_Three_Months(self):
        if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("返回 ")') != []:
            logging.info(self.deviceid + u'-出现三个月,重新返回')
            if self.phmode == '14.玉米平台'.decode("utf-8"):
                self.ph.yumi_cancelSMSRecv(self.phonenumber[0], self.phonenumber[1])
            return '1'
        if self.driver.find_elements_by_android_uiautomator('操作超时，请重新发起(错误码: -22)') != []:
            logging.info(self.deviceid + u'-操作超时')
            if self.phmode == '14.玉米平台'.decode("utf-8"):
                self.ph.yumi_cancelSMSRecv(self.phonenumber[0], self.phonenumber[1])
            return '1'


    #成功跳码
    def successful_Skip_Code(self):
        if self.driver.find_elements_by_id(self.element_json['czl'])!=[]:
            logging.info(self.deviceid + u'-跳码成功')
            return True

    #跳码失败直接退出
    def skip_Code_fail(self, error_type=None):
        if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("让用户用微信扫描下面的二维码")') != []:
            if error_type == 'Continue':
                logging.info(self.deviceid + u'-跳转到二维码页面')
            return False
        if self.driver.find_elements_by_name('让用户用微信扫描下面的二维码')!=[]:
            if error_type == 'Continue':
                logging.info(self.deviceid + u'-跳转到二维码页面')
            return False
    # 国内图片验证
    def yztp(self):
        """
        验证图片 
        """
        if self.tm == '9':
            while True:
                if self.driver.find_elements_by_name('安全校验') != []:
                    if self.skip_Code_fail() == False:
                        return False
                    if self.error_Three_Months() == '1':
                        return '1'
                if self.driver.find_elements_by_id(self.element_json[u'短信内容ID']) != []:
                    return True
                if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("开始 ")') != []:
                    os.popen('adb -s %s shell input swipe 50 1000 1000 1000 3000' % self.deviceid)
        if self.tm == '6':
            while True:
                try:
                    for j in range(101, 200, 30):
                        a = TouchAction(self.driver)
                        a.press(x=250, y=1000)
                        for i in range(0, 5):
                            a.move_to(x=50, y=(random.randint(-500, 0))).wait(0)
                            a.move_to(x=50, y=(random.randint(0, 500))).wait(0)
                        for i in range(0, j / 10):
                            a.move_to(x=10, y=0).wait(100)
                        a.release().perform()
                        self.Judgment_Devices()
                        if self.driver.find_elements_by_name('安全校验') != []:
                            if self.skip_Code_fail('Continue') == False:
                                return False
                            if self.error_Three_Months() == False:
                                return False
                        self.Judgment_Devices()
                        if self.driver.find_elements_by_id(self.element_json[u'短信内容ID']) != []:
                            return True
                        if self.driver.find_elements_by_name('开始 ') != []:
                            os.popen('adb -s %s shell input swipe 50 1000 1000 1000 3000' % self.deviceid)
                        if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("开始 ")') != []:
                            os.popen('adb -s %s shell input swipe 50 1000 1000 1000 3000' % self.deviceid)
                        if self.driver.find_elements_by_name('开始') != []:
                            os.popen('adb -s %s shell input swipe 50 1000 1000 1000 3000' % self.deviceid)
                        if self.driver.find_elements_by_android_uiautomator('new UiSelector().description("开始")') != []:
                            os.popen('adb -s %s shell input swipe 50 1000 1000 1000 3000' % self.deviceid)
                except:pass
    #任务确认
    def task_validation(self):
        """
        任务确认 
        """
        time.sleep(5)
        token = TokenYZ.pdtoken()
        status = submissionorder().confirm(self.deviceid, self.taskid, token)
        if status == '成功':
            logging.info(self.deviceid+u'-任务已确认完成')
        else:
            token = TokenYZ.pdtoken()
            status = submissionorder().confirm(self.deviceid, self.taskid, token)
            if status == '成功':
                logging.info(self.deviceid+u'-任务已确认完成')
        logging.info(self.deviceid + u'-正在发送短信')

    #等待扫码
    def waiting_code(self, end_time):
        self.driver.implicitly_wait(5)
        for self.i in range(1, int(end_time)):
            try:
                TouchAction(self.driver).tap(element=None, x=500, y=900).perform()
                self.dx = re.findall('[a-z0-9]{1,10}', self.driver.find_element_by_id(self.element_json[u'短信内容ID']).get_attribute(("text")))[0]
                logging.info(self.deviceid + u'-提取的发送内容为' + self.dx)
                self.task_validation()
                return True
            except:
                logging.info(self.deviceid + u'-扫码剩余时长' + str(end_time * 5 - self.i * 5))
                if self.i == end_time - 1:
                    token = TokenYZ.pdtoken()
                    submissionorder().fail(self.deviceid, self.taskid, token)
                    logging.info(self.deviceid + u'-辅助并未扫描成功,等待时间已过,重新注册!')
                    if self.tm == 'tm7':
                        if self.phmode == '14.玉米平台'.decode("utf-8"):
                            self.ph.yumi_cancelSMSRecv(self.phonenumber[0], self.phonenumber[1])
                    if self.phmode == '3.火箭API'.decode("utf-8"):
                        return self.ph.hj_fail(TokenYZ.pdtoken(), self.phonenumber[1])
                    self.driver.quit()
                    return False
    #切换VPN
    def switching_VPN(self):
        os.system('adb -s ' + self.deviceid + ' shell am force-stop org.proxydroid')
        os.system('adb -s ' + self.deviceid + ' shell am force-stop it.colucciweb.sstpvpnclient')

    def pd_ip(self, m):
        if self.switchingmode == '3.不换IP'.decode("utf-8"):
            self.ip =  os.popen('adb -s %s shell curl "http://ip.cip.cc'%self.deviceid).read()[0]
            return self.ip
        if self.switchingmode == '4.私人VPN'.decode('utf-8'):
            return self.wj.start(m,self.t,self.filtering_mode)

    #打开影子科技
    def start_yz(self):
        os.popen('adb -s ' + self.deviceid + ' shell am force-stop wechatscancoder.jionego.com.wechatscancoder')
        os.popen('adb -s %s shell am start -n wechatscancoder.jionego.com.wechatscancoder/.MainActivity' % self.deviceid).read()
        time.sleep(3)
        os.popen('adb -s %s shell am start -n com.tencent.mm/.ui.LauncherUI' % self.deviceid).read()

     #获取二维码图片
    def get_qr_image(self):
        folder = os.path.exists('./%s' % self.deviceid)
        if not folder:
            os.makedirs('./%s' % self.deviceid)
        else:
            pass
        res = requests.get('http://193.112.218.104:89/api?str=Initialize').text
        image = json.loads(res)['qrcode']
        data_62 = json.loads(res)['data']
        h = open("./%s/%s.jpg" % (self.deviceid, self.deviceid), "wb")
        h.write(base64.b64decode(image))
        h.close()
        os.popen('adb -s %s push ./%s/%s.jpg  /sdcard/myData/%s.jpg' % (self.deviceid, self.deviceid, self.deviceid,self.deviceid)).read()
        time.sleep(2)
        os.popen('adb -s %s shell mv /sdcard/myData/%s.jpg /sdcard/myData/scan.jpg' % (self.deviceid, self.deviceid)).read()
        time.sleep(2)
        os.system('adb -s %s shell curl http://127.0.0.1:8089?api=scandCode' % self.deviceid)
        return data_62


    #国内判断跳码
    def qr_validation(self, status):
        """
        判断是否跳码成功
        """
        if status == '1':
            self.driver.quit()
        if status == False:
            if self.tm == '9' or self.tm == '6':
                logging.info(self.deviceid + u'-未跳码成功,重新注册!')
                if self.phmode == '3.火箭API'.decode("utf-8"):
                    self.ph.hj_fail(TokenYZ.pdtoken(), self.phonenumber[1])
                if self.phmode == '9.老九专属API'.decode("utf-8"):
                    file().wite_lj_NotHopCode(self.phonenumber[0])
                if self.phmode == '2.菜鸟平台'.decode('utf-8'):
                    self.ph.cn_lh(self.phonenumber[0], self.phonenumber[1])
                if self.phmode == '12.国内私人3'.decode('utf-8'):
                    self.ph.grsr3_lh(self.phonenumber[1])
                if self.phmode == '13.国内私人4'.decode('utf-8'):
                    self.ph.grsr4_lh(self.phonenumber[1])
                self.driver.quit()
            else:
                self.Submission_Task()
                if self.cooperator == '1.火箭辅助'.decode("utf-8"):
                    if self.waiting_code(72) == True:
                        if self.phmode == '14.玉米平台'.decode("utf-8"):
                            return self.yumi_sendmsg(self.dx)
                        if self.phmode == '3.火箭API'.decode("utf-8"):
                            if self.ph.send_text(TokenYZ.pdtoken(), self.phonenumber[1], self.dx) == True:
                                return 'succ'
                        if self.phmode == '1.小鱼平台'.decode('utf-8'):
                            return self.ph.xiaoyu_send_message(self.phonenumber[0], self.dx)
                        if self.phmode == '13.国内私人4'.decode('utf-8'):
                            return self.ph.grsr4_send(self.phonenumber[1], self.dx)
                    else:
                        return False
        if status == True:
            dx = re.findall('[a-z0-9]{1,10}', self.driver.find_element_by_id(self.element_json[u'短信内容ID']).get_attribute(("text")))[0]
            logging.info(self.deviceid + u'-读取的短信内容为:' + dx)
            if self.phmode == '14.玉米平台'.decode("utf-8"):
                return self.yumi_sendmsg(dx)
            if self.phmode == '2.菜鸟平台'.decode('utf-8'):
                return self.ph.cn_send(self.phonenumber[1], dx)
            if self.phmode == '3.火箭API'.decode("utf-8"):
                #如果火箭平台返回True代表发送成功
                hj_status = self.ph.send_text(TokenYZ.pdtoken(), self.phonenumber[1], dx)
                if hj_status == True:
                    # 如果火箭平台返回True则返回一个succ
                    return 'succ'
            if self.phmode == '7.辽宁API'.decode("utf-8"):
                ln_status=self.ph.ln_send(self.phonenumber[0], dx)
                if ln_status == True:
                    return 'succ'
            if self.phmode == '8.国内私人1'.decode("utf-8"):
                return self.ph.gnsr_send_text(self.phonenumber[0], dx)
            if self.phmode == '9.老九专属API'.decode("utf-8"):
                return self.ph.lj_send_text(self.phonenumber[0], dx)
            if self.phmode == '10.国内私人2'.decode('utf-8'):
                return self.ph.gnsr2_send(self.phonenumber[0], dx)
            if self.phmode == '12.国内私人3'.decode('utf-8'):
                return self.ph.grsr3_send(self.phonenumber[1], dx)
            if self.phmode == '13.国内私人4'.decode('utf-8'):
                return self.ph.grsr4_send(self.phonenumber[1], dx)
            if self.phmode == '1.小鱼平台'.decode('utf-8'):
                return self.ph.xiaoyu_send_message(self.phonenumber[0], dx)
    #提交任务
    def Submission_Task(self):
        """
        提交任务订单
        """
        self.driver.implicitly_wait(180)
        self.driver.execute()
        logging.info(self.deviceid + u'-获取二维码')
        logging.info(self.deviceid + u'-正在解析二维码')
        url = analysis().get(self.deviceid)
        token = TokenYZ.pdtoken()
        logging.info(self.deviceid + u'-二维码解析地址:%s' % url)
        if self.phmode == '3.火箭API'.decode("utf-8"):
            self.taskid = submissionorder().submission_hj(url, self.phonenumber[0], token, '360', self.phonenumber[1])
        else:
            self.taskid = submissionorder().submission(url, self.phonenumber[0], token, '360')
        logging.info(self.deviceid + u'-订单提交成功')
        logging.info(self.deviceid + u'-订单号:' + self.taskid)
        self.driver.implicitly_wait(5)
    #玉米发短信
    def yumi_sendmsg(self, dx):
        try:
            yz = self.ph.yumi_sendmessages(dx, self.phonenumber[0], self.phonenumber[1])
            return yz
        except:
            logging.info(self.deviceid + u'-短信发送失败,卡商已下卡')

    #国外登录
    def gw_login_validation(self):
        self.driver.implicitly_wait(2)
        while True:
            if self.driver.find_elements_by_name(self.element_json['Two_registration'])!=[]:
                logging.info(self.deviceid + u'-判断是否二次注册')
                self.driver.find_element_by_name(self.element_json['Two_registration']).click()
                self.driver.implicitly_wait(10)
                if self.driver.find_elements_by_name(self.element_json['OK'])!=[]:
                    raise Exception(logging.info(self.deviceid + u'-出现错误,重新注册'))
                logging.info(self.deviceid + u'-该账号为二次注册')
            if self.driver.find_elements_by_name(self.element_json['WeChat'])!=[]:
                logging.info(self.deviceid + u'-已进入到微信页面')
                if self.gj_mode == '1.微霸改机'.decode("utf-8"):
                    self.wxid = self.w.get_wxid()
                    self.cloudCode = self.w.getCloudCode(self.phonenumber[0])
                    self.xr_wechat(self.wxid, self.cloudCode, 'True')
                    logging.info(self.deviceid + u'-注册数据已写入文件')
                    logging.info(self.deviceid + u'-正在保存微霸数据请稍等')
                    if self.w.save_wechat_data(self.phonenumber[0], self.wxid, self.wxmc) == True:
                        break
                else:
                    self.xr_wechat(mf='True')
                    logging.info(self.deviceid + u'-注册数据已写入文件')
                    break
            if self.driver.find_elements_by_name(self.element_json['OK']) != []:
                self.driver.find_element_by_name(self.element_json['OK']).click()
                self.driver.implicitly_wait(10)
                if self.driver.find_elements_by_name(self.element_json['allow'])!=[]:
                    self.driver.find_element_by_name(self.element_json['allow']).click()
            if self.driver.find_elements_by_id(self.element_json[u'输入框ID'])!=[]:
                raise Exception(logging.info(self.deviceid + u'-账号秒封'))

    def T_A16(self,A16):
            file().write('%s|%s|%s|%s|%s|%s|%s|%s|\n' % (self.phonenumber[0], self.wxmm,A16, self.IMEI,self.ANDROID_ID ,self.MAC, self.CPU_ABI,self.Brand), 'A16数据.txt')
            logging.info(u'%s-提62成功' % self.deviceid)

    def scanCode(self,A16):
        if token().huojian_t62(self.deviceid, TokenYZ.pdtoken()) == True:
            self.T_A16(A16)

    #写入文件
    def xr_wechat(self,wxid=None,cloudCode=None,mf=None):
            wechat_list = '%s_%s  %s  %s  %s  %s  %s|\n' % (self.phonenumber[0], self.wxmm, self.ip, self.deviceid, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), wxid,cloudCode )
            file().write(wechat_list, '微信账号数据.txt')

    def send_login(self):
            if self.phmode == '8.国内私人1'.decode("utf-8"):
                self.ph.qg_card_add(TokenYZ.pdtoken(), self.phonenumber[0])
            time.sleep(8)
            self.driver.implicitly_wait(60)
            logging.info(self.deviceid + u'-短信发送成功')
            if self.driver.find_elements_by_name('已发送短信，下一步')!=[]:
                self.driver.find_element_by_name('已发送短信，下一步').click()
            # 判断是否发送短信失败,点击下一步
            while True:
                self.driver.implicitly_wait(2)
                self.Judgment_Devices()
                if self.driver.find_elements_by_name('不是我的，继续注册')!=[]:
                    self.driver.find_element_by_name('不是我的，继续注册').click()
                self.Judgment_Devices()
                if self.driver.find_elements_by_id(self.element_json[u'输入框ID'])!=[]:
                    self.driver.quit()
                    break
                self.Judgment_Devices()
                if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID']) != []:
                    self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
                    if '短信' in self.cw.encode('utf-8'):
                        self.driver.find_element_by_id(self.element_json[u'错误弹窗确定ID']).click()
                        time.sleep(25)
                        self.driver.find_element_by_name('已发送短信，下一步').click()
                        time.sleep(20)
                        if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID'])!=[]:
                            self.cw = self.driver.find_element_by_id(self.element_json[u'错误弹窗内容ID']).get_attribute(('text'))
                            if '短信' in self.cw.encode('utf-8'):
                                logging.info(self.deviceid + u'-已点击过"已发送短信，下一步"两次,还是未注册成功,进入重新注册流程')
                                self.driver.quit()
                            if '逻辑' in self.cw.encode('utf-8'):
                                self.driver.find_element_by_id(self.element_json[u'错误弹窗确定ID']).click()
                                logging.info(self.deviceid + u'-已进入到微信页面,等待5秒判断是否出现秒封状况')
                                self.driver.implicitly_wait(5)
                                if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID']) != []:
                                    logging.info(self.deviceid + u'-账号秒封,重新注册')
                                else:
                                    if self.gj_mode == '1.微霸改机'.decode("utf-8"):
                                        self.save_wechat_data()
                                        if self.w.save_wechat_data(self.phonenumber[0], self.wxid, self.wxmc) == True:
                                            break
                                    if self.gj_mode == '测试'.decode("utf-8"):
                                        self.driver.implicitly_wait(50)
                                        self.driver.find_element_by_name('我').click()
                                        wxid = re.findall('(wxid_[0-9a-z]{1,100})', self.driver.find_element_by_id('com.tencent.mm:id/cl8').get_attribute(("text")))[0]
                                        logging.info('%s-微信ID:%s'%(self.deviceid,wxid))
                                        self.driver.find_element_by_name('微信').click()
                                        self.sandbox_save(wxid)
                                    else:
                                        self.xr_wechat(mf='True')

                                        logging.info(self.deviceid + u'-注册数据已写入文件')
                                        break
                    if '异常' in self.cw.encode('utf-8'):
                        logging.info(self.deviceid + u'-该账号被秒封')
                        if self.gj_mode == '1.微霸改机'.decode("utf-8"):
                            self.save_wechat_data()
                            if self.w.save_wechat_data(self.phonenumber[0], self.wxid, self.wxmc) == True:
                                break
                    if '逻辑' in self.cw.encode('utf-8'):
                        self.driver.find_element_by_id(self.element_json[u'错误弹窗确定ID']).click()
                        logging.info(self.deviceid + u'-已进入到微信页面,等待5秒判断是否出现秒封状况')
                        self.driver.implicitly_wait(5)
                        if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID']) != []:
                            logging.info(self.deviceid + u'-账号秒封,重新注册')
                        else:
                            if self.gj_mode == '1.微霸改机'.decode("utf-8"):
                                self.save_wechat_data()
                                if self.w.save_wechat_data(self.phonenumber[0], self.wxid, self.wxmc) == True:
                                    break
                            else:
                                self.xr_wechat(mf='True')
                                logging.info(self.deviceid + u'-注册数据已写入文件')
                                break
                    if '一个月' in self.cw.encode('utf-8'):
                        logging.info(self.deviceid + u'-该手机号码一个月之内不能重复注册')
                        self.driver.quit()
                    if '当天' in self.cw.encode('utf-8'):
                        logging.info(self.deviceid + u'-该手机号码当天不能重复注册')
                        os.popen('adb -s %s shell input keyevent 4' % self.deviceid).read()
                        time.sleep(3)
                        os.popen('adb -s %s shell input keyevent 4' % self.deviceid).read()
                        self.driver.implicitly_wait(60)
                        if self.driver.find_elements_by_id(self.element_json[u'输入框ID'])!=[]:
                            os.popen('adb -s %s shell input keyevent 4' % self.deviceid).read()
                            if self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID'])!=[]:
                                pass
                    if '不正确' in self.cw.encode('utf-8'):
                        logging.info(self.deviceid + u'-发送的验证码不正确')
                        self.driver.quit()
                    if '近期' in self.cw.encode('utf-8'):
                        logging.info(self.deviceid + u'-近期相同号码不可重复注册')
                        self.driver.quit()
                self.Judgment_Devices()
                if self.driver.find_elements_by_name('微信') != []:
                    logging.info(u'%s-已进入到微信页面,等待5秒判断是否出现秒封状况'%self.deviceid)
                    self.driver.implicitly_wait(5)
                    if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID']) != []:
                        logging.info(self.deviceid + u'-账号秒封,重新注册')
                    else:
                        if self.gj_mode == '测试'.decode('utf-8'):
                            self.driver.implicitly_wait(180)
                            self.driver.find_element_by_name('我').click()
                            wxid = re.findall('(wxid_[0-9a-z]{1,100})',self.driver.find_element_by_id('com.tencent.mm:id/czz').get_attribute(("text")))[0]
                            self.driver.find_element_by_name('微信').click()
                            self.driver.keyevent(4)
                            while True:
                                if self.driver.find_elements_by_id('com.dobe.sandbox:id/appIcon')!=[]:
                                    self.driver.find_element_by_id('com.dobe.sandbox:id/appIcon').click()
                                if self.driver.find_elements_by_name('微信')!=[]:
                                    break
                            #self.q(wxid)
                            self.sandbox_save(wxid)
                            break
                        else:
                            self.xr_wechat(mf='True')
                            logging.info(self.deviceid + u'-注册数据已写入文件')
                            break
                #os.popen('adb -s %s shell am start -n com.dobe.sandbox/.home.Main2Activity' % self.deviceid)
                #self.Judgment_Devices()
                #time.sleep(2)
                #self.driver.implicitly_wait(30)
                #if self.driver.find_elements_by_id('com.dobe.sandbox:id/context_menu')!=[]:
                #    self.driver.find_element_by_id('com.dobe.sandbox:id/context_menu').click()
                #    self.Judgment_Devices()
                #    self.driver.find_element_by_name('关闭进程').click()
                #    self.Judgment_Devices()
                #    self.driver.find_element_by_name('确认关闭').click()
                #    time.sleep(3)
                #    if self.driver.find_elements_by_id('com.dobe.sandbox:id/appIcon')!=[]:
                #        self.driver.find_element_by_id('com.dobe.sandbox:id/appIcon').click()
                #        time.sleep(5)

    def q(self,wxid):
        self.driver.implicitly_wait(2)
        while True:
            if self.driver.find_elements_by_id(self.element_json[u'错误弹窗确定ID']) != []:
                self.driver.quit()
                break
            if self.driver.find_elements_by_id(self.element_json[u'首页注册ID']) != []:
                logging.info(self.deviceid + u'-账号被秒封')
                self.driver.quit()
                break
            if self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID']) != []:
                self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID'])[2].click()
                logging.info(self.deviceid + u'-点击发现')
                break
            if self.driver.find_elements_by_id(self.element_json[u'输入框ID']) != []:
                logging.info(self.deviceid + u'-账号被秒封')
                self.driver.quit()
        time.sleep(random.randint(1, 3))
        self.driver.implicitly_wait(10)
        if self.gj_mode == '测试'.decode("utf-8"):
            wechat_list = '%s_%s  %s  %s  %s  %s  \n' % (self.phonenumber[0], self.wxmm, self.ip, self.deviceid, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), wxid )
            file().write(wechat_list, '微信账号数据(不带环境包).txt')
        if self.driver.find_elements_by_name('朋友圈') != []:
            self.driver.find_element_by_name('朋友圈').click()
            time.sleep(random.randint(1, 3))
        else:
            logging.info(self.deviceid + u'-点击发现失败,重新点击')
            self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID'])[2].click()
            self.driver.find_element_by_name('朋友圈').click()
        time.sleep(random.randint(1, 3))
        if self.driver.find_elements_by_id(self.element_json[u'朋友圈相机ID']) != []:
            TouchAction(self.driver).long_press(self.driver.find_element_by_id(self.element_json[u'朋友圈相机ID']),3000).release().perform()
        time.sleep(random.randint(1, 3))
        self.driver.implicitly_wait(5)
        # 检测有没有朋友圈
        if self.driver.find_elements_by_id(self.element_json[u'发表按钮ID']) != []:
            self.input_pyq_message()
        else:
            time.sleep(random.randint(1, 2))
            self.driver.find_element_by_id(self.element_json[u'我知道了ID']).click()
            self.input_pyq_message()
        logging.info(self.deviceid + u'-点击发表')
        self.driver.implicitly_wait(60)
        time.sleep(random.randint(1, 2))
        self.driver.find_element_by_android_uiautomator(
            'new UiSelector().description("返回")').click()
        time.sleep(random.randint(1, 2))
        self.driver.find_elements_by_id(self.element_json[u'微信四个主按钮ID'])[0].click()
        time.sleep(3)

    def sandbox_save(self,wxid):
        os.system('adb -s ' + self.deviceid + ' shell am force-stop org.wuji')
        self.driver.keyevent(4)
        #os.popen('adb -s %s shell am start -n com.dobe.sandbox/.home.Main2Activity'%self.deviceid)
        self.driver.implicitly_wait(50)
        self.Judgment_Devices()
        self.driver.find_element_by_id('com.dobe.sandbox:id/context_menu').click()
        self.Judgment_Devices()
        self.driver.find_element_by_name('关闭进程').click()
        self.Judgment_Devices()
        self.driver.find_element_by_name('确认关闭').click()
        self.Judgment_Devices()
        time.sleep(2)
        self.driver.find_element_by_id('com.dobe.sandbox:id/download_device').click()
        self.Judgment_Devices()
        self.driver.find_element_by_name('备份恢复').click()
        self.Judgment_Devices()
        self.driver.find_element_by_name('+ 创建备份').click()
        self.Judgment_Devices()
        os.popen('adb -s %s shell input text %s' % (self.deviceid, self.phonenumber[0]))
        self.Judgment_Devices()
        self.driver.find_element_by_name('确定').click()
        time.sleep(5)
        while True:
            time.sleep(2)
            if len(self.driver.find_elements_by_class_name('android.widget.ImageView')) < 2:
                logging.info(u'%s-数据备份完成' % self.deviceid)
                break
        time.sleep(5)
        self.new_package = re.findall('(.*?).zip', os.popen('adb -s %s shell ls /sdcard/boxbackup' % self.deviceid).read().strip('\n'))[0]
        self.xr_wechat(wxid=wxid, cloudCode = self.new_package + '.zip')
        logging.info(self.deviceid + u'-注册数据已写入文件')
        os.popen(
            'start adb -s %s pull /sdcard/boxbackup/%s.zip package/%s/%s.zip' % (self.deviceid, self.new_package,self.deviceid,self.new_package))
        while True:
            try:
                f = zipfile.ZipFile("package/%s/%s.zip" % (self.deviceid, self.new_package), 'r')
                for file in f.namelist():
                    f.extract(file, "package/%s/0" % self.deviceid)
                break
            except:pass
        time.sleep(2)
        file_data = open('package/%s/0/0/hook/data.json' % self.deviceid, 'r').read()
        self.CPU_ABI = json.loads(file_data)['CPU_ABI']
        logging.info('%s-CPU_ABI:%s' % (self.deviceid, self.CPU_ABI))
        self.ANDROID_ID = json.loads(file_data)['android_id']
        logging.info('%s-ANDROID_ID:%s' % (self.deviceid, self.ANDROID_ID))
        A16_list = []
        for filename in os.listdir('package/%s/0/0/com.tencent.mm/files/kvcomm/' % self.deviceid):
            try:
                with open('package/%s/0/0/com.tencent.mm/files/kvcomm/%s' % (self.deviceid, filename), 'r') as f:
                    A16 = re.findall(
                        '(A[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z])',
                        f.read())
                    if A16 != []:
                        A16_list.append(A16[0])
            except:
                pass
        Notes = zipfile.ZipFile(r'package/%s/%s.zip'%(self.deviceid,self.new_package), 'r').comment
        list = ['app_tbs', 'lib','tinker']
        logging.info(u'%s-A16:%s' % (self.deviceid, A16_list[0]))
        self.scanCode(A16_list[0])
        for i in list:
            try:
                Pack.remove_dir('package/%s/0/0/com.tencent.mm/%s' % (self.deviceid,i))
            except:pass
        for i in range(100,1000):
            try:
                Pack.remove_dir('package/%s/0/0/com.tencent.mm/app_xwalk_%s' % (self.deviceid, i))
            except:pass
        shutil.make_archive('package/%s/%s' % (self.deviceid,self.new_package), 'zip', r'package/%s/0'%(self.deviceid))
        zf = zipfile.ZipFile('package/%s/%s.zip' % (self.deviceid,self.new_package), 'a')
        zf.comment = Notes
        zf.close()
        time.sleep(2)
        try:
            Pack.remove_dir('package/%s/0'%self.deviceid)
        except:pass
        os.popen('adb -s %s rm -rf /sdcard/boxbackup' % self.deviceid)

    def save_wechat_data(self):
        self.wxid = self.w.get_wxid()
        self.cloudCode = self.w.getCloudCode(self.phonenumber[0])
        self.xr_wechat(self.wxid, self.cloudCode, 'True')
        logging.info(self.deviceid + u'-注册数据已写入文件')
        logging.info(self.deviceid + u'-正在保存微霸数据请稍等')
    # 国内登录
    def login_validation(self, yz):
        if yz == None:
            self.driver.quit()
        if yz == 'succ':
            self.send_login()

    #国内发圈
    def fpyq(self, yz):
        if yz == None:
            self.driver.quit()
        if yz == 'succ':
            self.send_login()
        else:
            logging.info(self.deviceid + u'-未接收到卡商反馈，注册失败')

    def input_pyq_message(self):
        time.sleep(random.randint(1, 2))
        self.driver.find_element_by_id(self.element_json[u'朋友圈内容输入框ID']).click()
        try:
            self.driver.find_element_by_id(self.element_json[u'朋友圈内容输入框ID']).send_keys(file().sh())
        except:
            self.driver.find_element_by_id(self.element_json[u'朋友圈内容输入框ID']).send_keys('My name is daduizhang')
        logging.info(self.deviceid + u'-输入文字')
        time.sleep(random.randint(1, 2))
        self.driver.find_element_by_id(self.element_json[u'发表按钮ID']).click()
    def pd_gj(self):
        if self.gj_mode == '1.微霸改机'.decode("utf-8"):
            self.wb_new()
        if self.gj_mode == '2.神奇改机'.decode("utf-8"):
            self.dd_new()
        if self.gj_mode == '测试'.decode("utf-8"):
            self.sand_box()
    def new_zh(self):
        try:
            self.pd_gj()
            self.register()
            self.input_text()
            self.login_validation(self.qr_validation(self.yztp()))
        except:
            traceback.print_exc()
            logging.info(self.deviceid + u'-账号注册失败')

    def new_zhpyq(self):
        try:
            self.pd_gj()
            self.register()
            self.input_text()
            self.fpyq(self.qr_validation(self.yztp()))
        except:
            traceback.print_exc()
            logging.info(self.deviceid + u'-账号注册失败')

    def gw_zc_t62_1280(self):
        pass

    def zc_pyq_t62(self):
        try:
            self.pd_gj()
            if self.country == '1.国内'.decode("utf-8"):
                self.register()
                self.input_text()
                self.fpyq(self.qr_validation(self.yztp()))
        except:
            traceback.print_exc()
            logging.info(self.deviceid + u'-账号注册失败')
            try:
                if self.phmode == '3.火箭API'.decode("utf-8"):
                    self.ph.hj_fail(TokenYZ.pdtoken(), self.phonenumber[1])
            except:pass
