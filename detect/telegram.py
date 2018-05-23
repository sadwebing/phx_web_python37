#!/usr/bin/env python
#-_- coding:utf-8 -_-
#Author: Arno
#Introduction:
#    调用telegram API，发送信息

import requests, sys, os
import datetime, json, logging, re
from monitor.models import telegram_user_id_t
from phxweb import settings

logger = logging.getLogger('django')

# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#获取当前脚本路径
basedir = os.path.abspath(os.path.dirname(__file__))

#获取当前时间，以特定的格式，如Wed, 09 May 2018 12:51:25 GMT
def getDate():
    return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S   GMT')

#telegram 通知

class sendTelegram(object):
    def __init__(self, message):
        '''参数初始化'''
        tg         = settings.TELEGRAM_API
        bot        = message['bot'] if message.has_key('bot') else ''
        doc        = message['doc'] if message.has_key('doc') else False
        group      = message['group'] if message.has_key('group') else ''
        parse_mode = message['parse_mode'] if message.has_key('parse_mode') else 'HTML'
        timeout    = message['timeout'] if message.has_key('timeout') and isinstance(message['timeout'], int) else 15

        self.__message = {}
        self.__doc     = doc
        self.__timeout = timeout
        self.__url     = tg['url'][bot] if tg['url'].has_key(bot) else tg['url']['sa_monitor_bot']
        self.__message['chat_id']    = tg['chat_id'][group] if tg['chat_id'].has_key(group) else tg['chat_id']['arno_test']
        self.__message['parse_mode'] = parse_mode
        self.__message['text']       = message['text'] if message.has_key('text') else ''

    def send(self):
        try:
            if self.__doc:
                with open('warning.txt', 'w') as f:
                    for line in text.split('\n'):
                        f.writelines(line+'\r\n')
                self.__files = {'document': open('warning.txt', 'rb')}
                ret = requests.post(self.__url+'sendDocument', data=self.__message, files=self.__files, timeout=self.__timeout)
            else:
                ret = requests.post(self.__url+'sendMessage', data=self.__message, timeout=self.__timeout)
        except Exception, e:
            logger.error('Attention: send message failed!')
            logger.error(e.message)
            return False
        else:
            if ret.status_code == 200:
                logger.info('send message successfull!')
                return True
            else:
                logger.error('Attention: send message failed!')
                logger.error('%s: %s' %(ret.status_code, ret.content))
                return False