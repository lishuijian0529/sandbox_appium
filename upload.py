# -*- coding:utf-8 -*-
import os
import time,threading
import json
import logging
import logger
def run(device,token):
     print device
     while True:
         try:
             os.system('adb -s %s shell screencap -p /sdcard/Download/screen.png' % device)
             time.sleep(5)
             qr_code = os.popen(
                 "adb -s %s shell curl -X POST \\\"http://www.wwei.cn/qrcode-fileupload.html?op=index_jiema\\\" -F \\\"file=@/sdcard/Download/screen.png\\\" " % device).read()
             qr_url = json.loads(qr_code)['jiema']
             if 'weixin' in qr_url:
                 logging.info(u'%s-二维码解析地址:%s' % (device, qr_url))
                 logging.info(u'%s-正在上传任务' % device)
                 task_res = os.popen('adb -s %s shell curl -X POST -H \\\"Authorization:Bearer %s\\\" -H \\\"Content-Type:application/x-www-form-urlencoded\\\" \\\"http://api.91huojian.com/task?qrcode=%s&title=WX&describe=test&expire=300&phone=\\\" ' % (
                     device, token, qr_url)).read()
                 task_id = json.loads(task_res)['data']
                 logging.info(u'%s-获取到任务ID:%s' % (device, task_id))
                 for i in range(0, 200):
                     os.system('adb -s %s shell uiautomator dump /sdcard/Download/uidump.xml' % device)
                     time.sleep(3)
                     ui_data = os.popen('adb -s %s shell cat /sdcard/Download/uidump.xml' % device).read()
                     if "10690700367" in ui_data:
                         os.popen(
                             'adb -s %s shell curl \\\"http://api.91huojian.com/task/finish?taskId=%s\\\" -H \\\"Authorization:Bearer %s\\\" ' % (
                             device, task_id, token))
                         logging.info(u'%s-任务ID:%s确认完成' % (device, task_id))
                         break
                     if "com.tencent.mm:id/czk" in ui_data:
                         os.popen(
                             'adb -s %s shell curl \\\"http://api.91huojian.com/task/finish?taskId=%s\\\" -H \\\"Authorization:Bearer %s\\\" ' % (device, task_id, token))
                         logging.info(u'%s-任务ID:%s确认完成' % (device, task_id))
                         break
         except:
             pass

if __name__ == '__main__':
    devices = os.popen('adb devices').read().splitlines()
    device_list = []
    for i in range(1, devices.__len__()):
       if 'device' in devices[i]:
           if 'List' not in devices[i]:
               device_list.append(devices[i][:-7])
    if device_list== []:
       logging.info(u'未检测到设备' )
       time.sleep(10000)
    logging.info(u'检测到%s个设备:%s' % (len(device_list), device_list))
    token = json.loads(open('token.txt', 'r').read())['token']
    for device in device_list:
        threading.Thread(target=run,args=(device.strip('\n'), token)).start()
