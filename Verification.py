# -*- coding:utf-8 -*-
import time
import pika
import json
import os
with open('账号配置.txt'.decode('utf-8'), 'r')as f:
    data = json.loads(f.read())
def callback(ch, method, properties,body):
    try:
        res = json.loads(body)
        print body
        os.popen('adb shell input tap 891 97')
        time.sleep(1)
        os.popen('adb shell input text %s'%res['phone'])
        os.popen('adb shell input tap 360 299')
        time.sleep(1)
        os.popen('adb shell input tap 360 299')
        time.sleep(1)
        os.popen('adb shell input tap 353 1876')
        time.sleep(1)
        os.popen('adb shell input text %s' % res['message'])
        os.popen('adb shell input tap 1012 1874')
        os.popen('adb shell input tap 38 104')
        os.popen('adb shell input tap 38 104')
        os.popen('adb shell input tap 38 104')
    except:
        pass
print u'已连接上服务器'
while True:
    try:
        credentials = pika.PlainCredentials('huan', '123123')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('111.231.146.172', 5672, 'validate', credentials))
        channel = connection.channel()
        channel.queue_declare(queue=data['user'],durable=True)
        channel.basic_consume(callback,queue=data['user'],no_ack=True)
        channel.start_consuming()
    except:pass

