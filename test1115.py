#!/usr/bin/python
#-*- coding:utf-8 -*-

import time
import re
# a=os.popen('adb shell "ps|grep org.proxydroid"').read()
# b=a.split()[1]
# print b
with open('A16数据.txt'.decode('utf-8'),'r')as f:
    a= f.readlines()
with open('未出.txt'.decode('utf-8'),'r') as f:
    b= f.readlines()
list_b = []
list_a = []
for i in b:
    list_b.append(re.findall('[0-9]{11}',i)[0])
for i in a:
    list_a.append( re.findall('[0-9]{11}',i)[0])
list_y = []
list_n = []
list_c = list(set(list_b) ^ set(list_a))
print 'A16文本%s个数据'.decode('utf-8')%len(a)
print '未出文本%s个数据'.decode('utf-8')%len(b)
for i in list_c:
    for j in b:
        if i in j:
            list_n.append(j.strip('\n'))
for i in a:
    for j in b:
        try:
            if  re.findall('[0-9]{11}',i.strip('\n'))[0] in j:
                list_y.append('%s           %s'%(j.strip('\n'),i.strip('\n')))
        except:
            pass
with open('未出.txt'.decode('utf-8'),'w')as f:
    for i in list_y:
        f.write('%s\n'%i.strip('\n'))
with open('未出.txt'.decode('utf-8'),'a')as f:
    for i in list_n:
        f.write('%s\n' % i.strip('\n'))
print 'ok'
time.sleep(100)
