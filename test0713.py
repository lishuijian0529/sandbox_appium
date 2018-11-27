# -*- coding:utf-8 -*-
import threading
import os
from time import ctime,sleep
import logging
import logger
import json
import re
import zipfile
import datetime
import time
import json
import requests
import httplib
import urllib
from File import file
import time
import os
#linux
import os
import random
import string
import shutil
import traceback

a='13346994852_v97i9yap  121.228.179.253  53476787  2018-11-05 07:17:55  wxid_a233p8r29r5t22  DC822B67AD.zip|'
b=a.split()
for i in b:
    if 'zip'in i :
        print i[:-1]
