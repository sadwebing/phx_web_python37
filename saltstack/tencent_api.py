#!/usr/bin/env python
#-_- coding:utf-8 -_-
#Author: Arno
#Introduction:
#    调用腾讯云API，刷新腾讯云域名静态文件缓存
#version: 1.0 20180626 实现基本功能

import requests, sys, commands, os, random, operator
import datetime, json, time, logging, urllib
from phxweb          import settings
from detect.telegram import sendTelegram
#HMAC-SHA1加密
import hmac, hashlib, base64

logger = logging.getLogger('django')

#from urllib  import request,parse

# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#获取当前脚本路径
basedir = os.path.abspath(os.path.dirname(__file__))

#telegram 参数
message = settings.message_ONLINE

#获取当前时间，以特定的格式，如Wed, 09 May 2018 12:51:25 GMT
def getDate():
    return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S   GMT')

#接口
tencent_url = "cdn.api.qcloud.com/v2/index.php"

class tcApi(object):
    def __init__(self, secretid, secretkey):
        self.__secretid   = secretid
        self.__secretkey  = secretkey
        self.__httpmethod = "POST"
        self.__warning = "\r\n".join([ 
                'Attention: 腾讯云域名缓存清理失败，请检查:'
                '腾讯云URL:  + %s' %tencent_url,
                #'%s : %s' %(secretid, secretkey)
              ])

    def signkey(self, httpmethod, domains=None, uri=None):
        if uri:
            if uri == '/' or uri[-1] == '/':
                self.__type_f = 'dirs' #目录刷新
                self.__params['Action'] = "RefreshCdnDir"
            else:
                self.__type_f = 'urls' #文件刷新
        if domains:
            i = 0
            for domain in domains:
                self.__params[self.__type_f+"."+str(i)] = domain.rstrip('/') + uri
                i += 1

        #self.__params = dict(sorted(self.__params.items(),key=operator.itemgetter(0)))
        src_str = httpmethod + tencent_url + "?"
        ifFirst = True
        for key in sorted(self.__params.items(),key=operator.itemgetter(0)):
            if ifFirst:
                src_str += key[0] + "=" + str(key[1])
                ifFirst = False
            else:
                src_str += "&" + key[0] + "=" + str(key[1])
        logger.info(src_str)
        logger.info(self.__secretkey)
        self.__params['Signature'] = base64.b64encode(hmac.new(str(self.__secretkey), str(src_str), hashlib.sha1).digest())
        #self.__params['Signature'] = urllib.urlencode({'1': Signature}).split('=')[1]
        #for key in self.__params:
        #    if isinstance(self.__params[key], str):
        #        self.__params[key] = urllib.urlencode({'1': self.__params[key]}).split('=')[1]
        
    def getdomains(self):
        self.__warning = "\r\n".join([ 
                'Attention: 腾讯云域名获取失败，请检查:'
                '腾讯云URL:  + %s' %tencent_url,
                #'%s : %s' %(secretid, secretkey)
              ])
        self.__params    = {
            'Action':'DescribeCdnHosts',
            'Nonce': random.randint(1, 1000000),
            'SecretId':secretid,
            'Timestamp': int(time.time()),
        }
        self.signkey(self.__httpmethod)
        url = "https://" + tencent_url
        try:
            ret = requests.post(url, data=self.__params, verify=False)
        except Exception, e:
            message['text'] = self.__warning + '\nException: ' + e.message
            logger.error(message['text'])
            sendTelegram(message).send()
            return self.__params, False

        else:
            if ret.json()['code'] != 0:
                message['text'] = self.__warning + '\n' + ret.json()['message']
                logger.error(message['text'])
                sendTelegram(message).send()
                return ret.json(), False
        
            else:
                logger.info(str(self.__params)+": 腾讯云域名获取成功！")
                return ret.json(), True
        
    def purge(self, domains, uri="/"):
        self.__params    = {
            'Action':'RefreshCdnUrl',
            'Nonce': random.randint(1, 1000000),
            'SecretId':secretid,
            'Timestamp': int(time.time()),
        }
        self.signkey(self.__httpmethod, domains, uri)
        url = "https://" + tencent_url
        #logger.info(self.__params)
        try:
            ret = requests.post(url, data=self.__params, verify=False)
        except Exception, e:
            message['text'] = self.__warning + '\nException: ' + e.message
            logger.error(message['text'])
            sendTelegram(message).send()
            return self.__params, False

        else:
            if ret.json()['code'] != 0:
                message['text'] = self.__warning + '\n' + ret.json()['message']
                logger.error(message['text'])
                sendTelegram(message).send()
                return ret.json(), False
        
            else:
                logger.info(str(self.__params)+": 缓存清理成功！")
                return ret.json(), True


if __name__ == '__main__':
    print "腾讯云"
