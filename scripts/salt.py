#!/usr/bin/env python
#-_- coding:utf-8 -_-
import os,sys,datetime,logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
reload(sys)
sys.setdefaultencoding('utf8')
from monitor import settings
from saltstack.saltapi import SaltAPI
from scripts.tomcat import get_mail_list

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
#获取salt接口，接入rest接口，获取salt信息
sapi = SaltAPI(
    url      = settings.SALT_API['url'],
    username = settings.SALT_API['user'],
    password = settings.SALT_API['password']
    )

minionsup, minionsdown= sapi.MinionStatus()
