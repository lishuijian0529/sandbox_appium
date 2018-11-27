# -*- coding:utf-8 -*-
import re
import os
import logging
import requests
import json
class analysis():
    def get(self,device):
        while True:
            os.popen('adb -s ' + device + ' shell /system/bin/screencap -p /sdcard/test.jpg')
            os.popen('adb pull /sdcard/test.jpg image/%s.jpg'%device)
            data = {"file": ('%s.jpg'%device,open('image/%s.jpg'%device,'rb'),'image/jpg')}
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
            qr_url = json.loads(requests.post('http://www.wwei.cn/qrcode-fileupload.html?op=index_jiema', files=data, headers=header).text)[
                'jiema']
            if 'https' in qr_url:
                return qr_url




if __name__ == '__main__':
    print analysis().get('53476787')