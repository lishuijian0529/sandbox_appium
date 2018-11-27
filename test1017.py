
#-*- encoding:utf-8 -*-
from ftplib import FTP
#登陆FTP
import time
import os
import re
import json
import datetime
import zipfile
import shutil
f=zipfile.ZipFile("DC822B67AD.zip" , 'r')
for file in f.namelist():
    f.extract(file, "temp/DC822B67AD" )


def remove_dir(dir):
   dir = dir.replace('\\', '/')
   if(os.path.isdir(dir)):
       for p in os.listdir(dir):
           remove_dir(os.path.join(dir,p))
       if(os.path.exists(dir)):
           os.rmdir(dir)
   else:
       if(os.path.exists(dir)):
           os.remove(dir)

def run(package):
    path='temp/%s/0/com.tencent.mm'%package
    remove_dir('%s/app_cache'%path)
    remove_dir('%s/app_dex'%path)
    remove_dir('%s/app_icon_assets'%path)
    remove_dir('%s/app_lib'%path)
    remove_dir('%s/app_metadata'%path)
    remove_dir('%s/app_recover_lib'%path)
    remove_dir('%s/app_tbs'%path)
    remove_dir('%s/app_tbs_common_share'%path)
    remove_dir('%s/app_webviewcache'%path)
    remove_dir('%s/app_xwalk_359'%path)
    remove_dir('%s/app_xwalkplugin'%path)
    remove_dir('%s/cachetopstory'%path)
    remove_dir('%s/code_cache'%path)
    remove_dir('%s/face_detect'%path)
    remove_dir('%s/lib'%path)
    remove_dir('%s/tinker'%path)
    remove_dir('%s/tinker_server'%path)
    remove_dir('%s/tinker_temp'%path)
    remove_dir('%s/app_turingmm'%path)
    shutil.make_archive('package/%s/%s', 'zip', r'temp/DC822B67AD')
    zf = zipfile.ZipFile('package/%s/%s.zip', 'a')
    zf.comment = '011f8828507fc5d303fd51429cfec5d617bed08f2c1b24359657264b6d1094a557ea2e4b558109e42e13278cfc421d173fb003c1ba1a3db2986eb96f2b009e377a691a3276ab2568a4dfe646c75b80f7e6dd8a790929cabf5576312ee560260bd4510b356270cfbf3049ad7b6b9f5b17c24e56cc7ee0433036487d3841e23609'
    zf.close()
run('DC822B67AD')

shutil.make_archive('package/123/DC822B67AD', 'zip', r'temp/DC822B67AD')
zf = zipfile.ZipFile('package/123/DC822B67AD.zip', 'a')
zf.comment = '011f8828507fc5d303fd51429cfec5d617bed08f2c1b24359657264b6d1094a557ea2e4b558109e42e13278cfc421d173fb003c1ba1a3db2986eb96f2b009e377a691a3276ab2568a4dfe646c75b80f7e6dd8a790929cabf5576312ee560260bd4510b356270cfbf3049ad7b6b9f5b17c24e56cc7ee0433036487d3841e23609'
zf.close()
