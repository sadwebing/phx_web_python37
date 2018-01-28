#!/usr/bin/env python
#-_- coding:utf-8 -_-
#author: Arno
import os, sys, requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

#set django env settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'phxweb.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phxweb.settings")

from monitor.models import project_t, minion_t
from phxweb import settings
from saltstack.saltapi import SaltAPI
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#获取salt接口，接入rest接口，获取salt信息
sapi = SaltAPI(
    url      = settings.SALT_API['url'],
    username = settings.SALT_API['user'],
    password = settings.SALT_API['password']
    )


#minion_id_list = ['CP_NG_HK_83_36', 'CP_NG_HK_85_10', 'CP_NG_HK_34_106', 'CP_NG_HK_153_1', 'CP_NG_HK_179_204']
#minion_id_list = ['CP_NG_HK_50_4', 'CP_NG_HK_224_181', 'CP_NG_HK_224_152', 'CP_NG_HK_224_249']
#
#for minion_id in minion_id_list:
#    insert = project_t(
#        product = 'UC',
#        project = 'CAIPIAO',
#        minion_id = minion_id,
#        domain = 'uc22.com',
#        uri = '/',
#        info = 'high defense',
#    )
#    insert.save()


minion_id_list = ['CP_NG_HK_83_36', 'CP_NG_HK_85_10', 'CP_NG_HK_34_106', 'CP_NG_HK_153_1', 'CP_NG_HK_179_204', 'CP_NG_HK_50_4', 'CP_NG_HK_224_181', 'CP_NG_HK_224_152', 'CP_NG_HK_224_249']

for minion_id in minion_id_list:
    grains = sapi.GetGrains(minion_id)
    for ip in grains['return'][0][minion_id]['ipv4']:
        if ip == '127.0.0.1':
            continue
        elif ip[:7] == '192.168':
            continue
        select = minion_t.objects.filter(minion_id=minion_id, ip_addr=ip).all()
        if not select:
            insert = minion_t(
                minion_id = minion_id,
                ip_addr = ip,
            )
            insert.save()
