#!/usr//bin/env python
#-_- coding:utf-8 -_-
import os,sys,logging,datetime
import django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phxweb.settings")
django.setup()
from dns.models import cf_account, domain_info
from phxweb.settings import DATABASES as databases
from dns.cf_api import CfApi
from phxweb.settings import CF_URL

#获取当前目录
current_dir = os.path.abspath(os.path.dirname(__file__))
#print basedir

cursor = django.db.connection.cursor()

with open('%s/api_info.txt' %current_dir, 'r') as f:
    contents = f.readlines()
for info in contents:
    if not '#' in info and info.replace(' ', '') != '\n':
        cf_acc = cf_account.objects.filter(name=info.split()[3]).first()
        api = CfApi(CF_URL, cf_acc.email, cf_acc.key)
        zone_id = api.GetZoneId('.'.join(info.split()[2].split('.')[-2:]))['zone_id']
        record_id = api.GetDnsRecordId(zone_id, info.split()[2])



        try:
            #update = domain_info.objects.filter(product=info.split()[0], client=info.split()[1], domain=info.split()[2], route=info.split()[4]).first()
            #update = domain_info.objects.filter(product=info.split()[0], client=info.split()[1], domain=info.split()[2], content=info.split()[5]).first()
            #update.zone_id = zone_id
            #update.route = info.split()[4]
            #update.record_id = record_id
            #update.status = info.split()[6]
            #update.route_status = info.split()[7]
            #update.save()
            #print info.split()[0], info.split()[2], info.split()[4], 'update success.'

            insert = domain_info(product=info.split()[0], client=info.split()[1], domain=info.split()[2], cf_account_name=info.split()[3], route=info.split()[4], content=info.split()[5], status=info.split()[6], route_status=info.split()[7], zone_id=zone_id , record_id=record_id)
            insert.save()
            print info.split()[0], info.split()[2], info.split()[4],'insert success.'
        except:
            #print info.split()[0], info.split()[2], info.split()[4], 'update failed.'
            print info.split()[0], info.split()[2], info.split()[4], 'is already existing.'