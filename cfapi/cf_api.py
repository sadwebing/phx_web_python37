#!/usr/bin/env python
#-_- coding: utf-8 -_-
#author: arno
#introduction:
#    cfapi

import requests,json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import logging
logger = logging.getLogger('django')

class CfApi(object):
    def __init__(self, url, email, key):
        self.__url = url.rstrip('/')
        self.__email = email
        self.__key = key
        self.__headers = {'X-Auth-Email': self.__email, 'X-Auth-Key': self.__key, 'Content-Type': 'application/json'}

    def GetDnsRecords(self, zone_id):
        url = self.__url + '/%s/' %zone_id + 'dns_records?per_page=100'
        try:
            ret = requests.get(url, headers=self.__headers, verify=False)
            return ret.json()
        except:
            return {'result': []}

    def GetDnsRecordId(self, zone_id, record_name):
        self.__record_id = ''
        url = self.__url + '/%s/' %zone_id + 'dns_records?per_page=100&name=%s' %record_name
        try:
            ret = requests.get(url, headers=self.__headers, verify=False)
            if len(ret.json()['result']) == 0:
                pass
            elif len(ret.json()['result']) == 1:
                self.__record_id = ret.json()['result'][0]['id']
            else:
                self.__record_id = 'id more than one'
        except:
            self.__record_id = 'bad arguments'

        return self.__record_id

    def UpdateDnsRecords(self, zone_id, record_type, record_name, record_content, proxied=False):
        datas = {'type':record_type, 'name': record_name, 'content': record_content, 'proxied':proxied}
        record_id = self.GetDnsRecordId(zone_id, record_name)
        logger.info('record_id: %s' %record_id)

        if record_id == '':
            return {'result': 'id null'}
        elif record_id == 'id more than one':
            return {'result': 'id more than one'}
        elif record_id == 'bad arguments':
            return {'result': 'bad arguments'}
        else:
            url = self.__url + '/%s/' %zone_id + 'dns_records/'+ record_id
            try:
                ret = requests.put(url ,data=json.dumps(datas), headers=self.__headers, verify=False)
                return ret.json()
            except:
                return {'result': {}}

if __name__ == '__main__':
    print 'no'
