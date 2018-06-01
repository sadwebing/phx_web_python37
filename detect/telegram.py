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
        timeout    = message['timeout'] if message.has_key('timeout') and isinstance(message['timeout'], int) else 15

        self.__message = {}
        self.__doc     = doc
        self.__timeout = timeout
        self.__url     = tg['url'][bot] if tg['url'].has_key(bot) else tg['url']['sa_monitor_bot']
        self.__message['chat_id']    = tg['chat_id'][group]  if tg['chat_id'].has_key(group)  else tg['chat_id']['arno_test']
        self.__message['parse_mode'] = message['parse_mode'] if message.has_key('parse_mode') else ''
        self.__message['doc_name']   = message['doc_name']   if message.has_key('doc_name')   else 'warning.txt'
        self.__message['caption']    = self.getAtUsers(message['caption']) if message.has_key('caption') else ''
        self.__message['text']       = self.getAtUsers(message['text'])    if message.has_key('text') else ''
        self.__message['disable_web_page_preview'] = False if message.has_key('disable_web_page_preview') and message['disable_web_page_preview'].lower() == 'false' else True

    def getAtUsers(self, text):
        user_l = [ {'user': '@'+re.match('[a-z|A-Z]+(?![a-z])', user).group(), 
                    'name': re.match('[a-z]+(?![a-z])', user.lower()).group()} 
                    for user in text.split('@')[1:] if re.match('[a-z]+(?![a-z])', user.lower())]

        if self.__message['parse_mode'] == 'HTML':
            text = text.replace("<", "&lt;").replace(">", "&gt;")

        if user_l:
            user_id_l = {}
            s = telegram_user_id_t.objects.all()
            for i in s:
                user_id_l[i.user] = {}
                user_id_l[i.user]['name']    = i.name
                user_id_l[i.user]['user_id'] = i.user_id

            for user in user_l:
                if user_id_l.has_key(user['name']):
                    if self.__message['parse_mode'] == 'HTML':
                        atUser = "<a href='tg://user?id=%s'>%s</a>" %(user_id_l[user['name']]['user_id'], user_id_l[user['name']]['name'])
                        text = text.replace(user['user'], atUser)
                    elif self.__message['parse_mode'] == 'Markdown':
                        atUser = "[%s](tg://user?id=%s)" %(user_id_l[user['name']]['name'], user_id_l[user['name']]['user_id'])
                        text = text.replace(user['user'], atUser)

        #logger.info(text)
        return text

    def send(self):
        try:
            if (not self.__doc) or self.__doc.lower() == 'false':
                ret = requests.post(self.__url+'sendMessage', data=self.__message, timeout=self.__timeout)
            else:
                with open(self.__message['doc_name'], 'w') as f:
                    for line in self.__message['text'].split('\n'):
                        f.writelines(line+'\r\n')
                self.__files = {'document': open(self.__message['doc_name'], 'rb')}
                ret = requests.post(self.__url+'sendDocument', data=self.__message, files=self.__files, timeout=self.__timeout)
                
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