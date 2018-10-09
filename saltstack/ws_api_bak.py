#!/usr/bin/env python
#-_- coding:utf-8 -_-
#Author: Arno
#Introduction:
#    调用网宿API，刷新网宿域名静态文件缓存
#version: 1.0 20180626 实现基本功能

import requests, sys, commands, os
import datetime, hmac, base64, json
from hashlib import sha256
from phxweb  import settings

#from urllib  import request,parse

# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

rewrite_list = ['301', '302', '303']

#获取当前脚本路径
basedir = os.path.abspath(os.path.dirname(__file__))

#获取当前时间，以特定的格式，如Wed, 09 May 2018 12:51:25 GMT
def getDate():
    return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S   GMT')

#获取加密后的apikey
def signApikey(date, apikey):
    signed_apikey = hmac.new(apikey.encode('utf-8'), date.encode('utf-8'), sha256).digest()
    signed_apikey = base64.b64encode(signed_apikey)
    return signed_apikey

#获取有效的网宿域名
def getWsdomains(username, apikey):
    date    = getDate()
    headers = {'Date': date, 'Accept': 'application/json'}
    url     = 'https://open.chinanetcenter.com/api/domain'
    signed_apikey = signApikey(date, apikey)
    warning = "\r\n".join([ 
                'Attention: 获取网宿域名失败，请检查:'
                '网宿URL:  + %s' %url,
                'headers:  + %s' %headers,
                '%s : %s' %(username, signed_apikey)
              ])
    try:
        ret = requests.get(url, headers=headers, auth=(username, signed_apikey))

    except Exception as e:
        text = warning + '\nException: ' + e.message
        print (text)
        sendTelegram(text)
        return False

    else:
        if ret.status_code != 200:
            text = warning + '\n' + ret.content
            print (text)
            sendTelegram(text)
            return False

        else:
            #return [ line['domain-name'] for line in ret.json() if line['enabled'] == 'true']
            return [ line for line in ret.json() if line['enabled'] == 'true' and exclDomain(line['domain-name'])]

#排除域名
def exclDomain(domain):
    domain_l = ['alcpapi.com', 'gdcpapi.com', 'hhy988.com', 'fanyingsh.com']
    for dom in domain_l:
        if dom in domain: return False
    return True

#清理网宿域名缓存
def purgeWsdomains(domains, uri='/'):
    date    = getDate()
    headers = {'Date': date, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    url     = 'http://open.chinanetcenter.com/ccm/purge/ItemIdReceiver'
    signed_apikey = signApikey(date, apikey) #获取加密的签名
    warning = "\r\n".join([ 
                'Attention: 网宿域名缓存清理失败，请检查:'
                '网宿URL:  + %s' %url,
                'headers:  + %s' %headers,
                '%s : %s' %(username, signed_apikey)
              ])

    #判断是目录刷新还是文件刷新
    if uri == '/' or uri[-1] == '/':
        type_f = 'dirs' #目录刷新
    else:
        type_f = 'urls' #文件刷新

    data    = {type_f: []} #需要刷新的域名或者文件链接

    #格式化域名或者文件链接   
    for domain in domains:
        data[type_f].append('http://%s%s' %(domain['domain-name'], uri))
        #if domain['service-type'] == 'web-https':
        #    data[type_f].append('https://%s%s' %(domain['domain-name'], uri))

    try:
        ret = requests.post(url, headers=headers, auth=(username, signed_apikey), data=json.dumps(data))

    except Exception as e:
        text = warning + '\nException: ' + e.message
        print (text)
        sendTelegram(text)
        return data[type_f], False

    else:
        if ret.json()['Message'] != 'handle success':
            text = warning + '\n' + ret.content
            print (text)
            sendTelegram(text)
            return data[type_f], False

        else:
            return data[type_f], True
            #return data[type_f], str(ret.status_code) + ' : ' + ret.content


if __name__ == '__main__':
    print ("网宿")
