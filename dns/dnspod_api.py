#!/usr/bin/env python
#-_- coding: utf-8 -_-
#author: arno
#introduction:
#    dnspod api

from detect.telegram import sendTelegram
from phxweb          import settings
import requests, json, logging
logger = logging.getLogger('django')

# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#telegram 参数
message = settings.message_TEST

class DpApi(object):
    def __init__(self, url, key, format='json'):
        '''
            初始化接口参数，默认获取的数据格式为json
        '''
        self.__url  = url.rstrip('/')
        self.__key  = key
        self.__data = {
            'login_token': self.__key, #登陆token
            'format': format           #获取的数据格式
        }
        #self.__headers = {'X-Auth-Email': self.__email, 'X-Auth-Key': self.__key, 'Content-Type': 'application/json'}

        
    def ExePost(self, uri, info):
        url = self.__url + uri
        self.__warning = "\r\n".join([ 
                'Attention: %s 失败，请检查:' %info,
                'URL:  + %s' %url,
                #'%s : %s' %(secretid, secretkey)
              ])
        #logger.info(self.__data)
        try:
            ret = requests.post(url, data=self.__data, verify=False)
        except Exception, e:
            message['text'] = self.__warning + '\nException: ' + e.message
            logger.error(message['text'])
            sendTelegram(message).send()
            return error, False
        else:
            result = ret.json()
            if result['status']['code'] != "1":
                message['text'] = self.__warning + '\n' + str(result['status'])
                logger.error(message['text'])
                sendTelegram(message).send()
                return result, False
            else:
                logger.info("%s 成功！" %info)
                return result, True

    def GetDnsLists(self, type='all'):
        '''
            获取域名列表
        '''
        self.__data['type'] = type
        return self.ExePost('/Domain.List', "Dnspod域名列表获取")

    def GetZoneRecords(self, domain):
        '''
            获取域名解析记录
        '''
        self.__data['domain'] = domain
        return self.ExePost('/Record.List', "Dnspod域名[%s]解析获取" %domain)
        
    def DeleteZoneRecord(self, domain, record_id, full_domain):
        '''
            删除域名解析记录
        '''
        self.__data['domain']    = domain
        self.__data['record_id'] = record_id
        return self.ExePost('/Record.Remove', "Dnspod域名[%s]删除" %full_domain)
        
    def UpdateZoneRecord(self, domain, record_id, sub_domain, value, record_type, record_line_id, status):
        '''
            修改域名解析记录
        '''
        self.__data['domain']         = domain
        self.__data['record_id']      = record_id
        self.__data['sub_domain']     = sub_domain
        self.__data['value']          = value
        self.__data['record_type']    = record_type
        self.__data['record_line_id'] = record_line_id
        self.__data['status']         = status
        return self.ExePost('/Record.Modify', "Dnspod域名[%s]解析修改" %(sub_domain+'.'+domain))
        
if __name__ == '__main__':
    print 'no'