#!/usr//bin/env python
#-_- coding:utf-8 -_-
import os,sys,logging,datetime
import django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phxweb.settings")
django.setup()
from dns.models import domain_info
from phxweb.settings import DATABASES as databases

#获取当前目录
current_dir = os.path.abspath(os.path.dirname(__file__))
#print basedir

cursor = django.db.connection.cursor()

with open('%s/api_info.txt' %current_dir, 'r') as f:
    contents = f.readlines()
for info in contents:
    if not '#' in info and info.replace(' ', '') != '\n':
        #print info.split()[0], info.split()[1], info.split()[2], info.split()[3], info.split()[4], info.split()[5]
        try:
            insert = domain_info(product=info.split()[0], client=info.split()[1], domain=info.split()[2], cf_account_name=info.split()[3], route=info.split()[4], content=info.split()[5])
            insert.save()
        except:
            print info, 'is already existing.'