#!/usr/bin/env python
#-_- coding:utf-8 -_-
#Author: Arno
#Introduction:
#    调用telegram API，发送信息

import requests, sys, os
import datetime, json, logging, re

logger = logging.getLogger('django')

# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#获取当前脚本路径
basedir = os.path.abspath(os.path.dirname(__file__))

#telegram 参数
tg_api  = '471691674:AAFx1MQ3VwXdWUYyh4CaErzwoUNswG9XDsU'  # @AuraAlertBot api
tg_url  = 'https://api.telegram.org/bot%s/sendMessage' %tg_api
message = {} # 信息主体
message['chat_id'] = ''  # '-204952096': arno_test | '-275535278': chk_ng alert | '-317680977': 域名监控
message['text']    = ''

#获取当前时间，以特定的格式，如Wed, 09 May 2018 12:51:25 GMT
def getDate():
    return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S   GMT')

#telegram 通知
def sendTelegram(text, chat_id='-204952096' , doc=False, timeout=15):
    message['chat_id'] = chat_id
    if doc:
        with open('warning.txt', 'w') as f:
            for line in text.split('\n'):
                f.writelines(line+'\r\n')
        files = {'document': open('warning.txt', 'rb')}
        try:
            ret = requests.post(tg_url.replace('sendMessage', 'sendDocument'), data=message, files=files, timeout=timeout)
        except Exception, e:
            print 'Attention: send message failed!'
            print e.message

    else:
        message['text'] = text
        try:
            ret = requests.post(tg_url, data=message, timeout=timeout)
        except Exception, e:
            print 'Attention: send message failed!'
            print e.message