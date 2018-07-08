#!/usr/bin/env python
#-_- coding:utf-8 -_-
#Author: Arno
#Introduction:
#    调用网宿API，刷新网宿域名静态文件缓存
#version: 1.0 20180626 实现基本功能

import requests, sys, commands, os, logging
import datetime, hmac, base64, json
from hashlib import sha256
from phxweb  import settings
from detect.telegram import sendTelegram
#from urllib  import request,parse

logger = logging.getLogger('django')

# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

rewrite_list = ['301', '302', '303']

#telegram 参数
message = settings.message_ONLINE

#获取当前脚本路径
basedir = os.path.abspath(os.path.dirname(__file__))

#获取当前时间，以特定的格式，如Wed, 09 May 2018 12:51:25 GMT
def getDate():
    return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S   GMT')

class wsApi(object):
    def __init__(self, username, apikey):
        self.__username = username
        self.__apikey   = apikey

    def signApikey(self, date):
        '''
            获取加密后的apikey
        '''
        signed_apikey = hmac.new(self.__apikey.encode('utf-8'), date.encode('utf-8'), sha256).digest()
        signed_apikey = base64.b64encode(signed_apikey)
        return signed_apikey

        
    def getdomains(self):
        date = getDate()
        headers = {'Date': date, 'Accept': 'application/json'}
        url     = 'https://open.chinanetcenter.com/api/domain'
        signed_apikey = self.signApikey(date)
        self.__warning  = "\r\n".join([ 
                'Attention: 网宿域名获取失败，请检查:'
                '网宿URL:  + %s' %url,
                #'headers:  + %s' %headers,
                '%s : %s' %(self.__username, signed_apikey)
              ])
        try:
            ret = requests.get(url, headers=headers, auth=(self.__username, signed_apikey))
    
        except Exception, e:
            message['text'] = self.__warning + '\nException: ' + e.message
            logger.error(message['text'])
            sendTelegram(message).send()
            return {}, False
    
        else:
            if ret.status_code != 200:
                message['text'] = self.__warning + '\n' + str(ret.content.replace('<', '&lt;').replace('>', '&gt;'))
                logger.error(message['text'])
                sendTelegram(message).send()
                return ret.content, False
    
            else:
                logger.info("网宿域名获取成功！")
                return ret.json(), True

    def purge(self, domains, uri='/'):
        date = getDate()
        headers = {'Date': date, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        url     = 'http://open.chinanetcenter.com/ccm/purge/ItemIdReceiver'
        signed_apikey = self.signApikey(date)
        self.__warning = "\r\n".join([ 
                    'Attention: 网宿域名缓存清理失败，请检查:'
                    '网宿URL:  + %s' %url,
                    #'headers:  + %s' %headers,
                    '%s : %s' %(self.__username, signed_apikey)
                ])
    
        #判断是目录刷新还是文件刷新
        if uri == '/' or uri[-1] == '/':
            type_f = 'dirs' #目录刷新
        else:
            type_f = 'urls' #文件刷新
    
        data    = {type_f: []} #需要刷新的域名或者文件链接
    
        #格式化域名或者文件链接   
        for domain in domains:
            data[type_f].append('%s%s' %(domain, uri))
            #if domain['service-type'] == 'web-https':
            #    data[type_f].append('https://%s%s' %(domain['domain-name'], uri))
    
        try:
            ret = requests.post(url, headers=headers, auth=(self.__username, signed_apikey), data=json.dumps(data))
    
        except Exception, e:
            message['text'] = self.__warning + '\nException: ' + e.message
            logger.error(message['text'])
            sendTelegram(message).send()
            return {}, False
    
        else:
            if ret.json()['Message'] != 'handle success':
                message['text'] = self.__warning + '\n' + str(ret.json())
                logger.error(message['text'])
                sendTelegram(message).send()
                return ret.json(), False
            else:
                return ret.json(), True
                #return data[type_f], str(ret.status_code) + ' : ' + ret.content

if __name__ == '__main__':
    print "网宿"
