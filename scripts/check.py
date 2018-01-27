#!/usr/bin/env python
#-_- coding:utf-8 -_-
#author: Arno
#update: 2018/01/27  check_services_fun

import os,sys,datetime,logging,multiprocessing,requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor.settings")
#from monitor.models import check_status
from scripts.tomcat import logger, time, check_services, error_status, server
from time import sleep
#from saltstack.saltapi import SaltAPI
from phxweb import settings
from ctypes import c_char_p
from color_print import ColorP

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def check_services_fun():
    content = check_services()
    #check_services = check_status.objects.filter(program='check_services').first()
    #if check_services.status == 1:
    #    content = check_services()
    #    if content != "":
    #        send_mail(get_mail_list('check_services'),'tomcat报警',content,format='html')
    if content != "":
        message = {}
        url = settings.TG_API['url'] + '/sendMessage'
        message['chat_id'] = settings.TG_API['chat_id']['salt_minion_alert']
        message['text'] = content
        #message['parse_mode']='HTML'
        try:
            ret = requests.post(url, data=message, timeout=3)
        except:
            print 'send message failed.'
    end_time['check_services'] = time()

def check_salt_minion_fun():
    check_salt_minion = check_status.objects.filter(program='check_salt_minion').first()
    if check_salt_minion.status == 1:
        sapi = SaltAPI(
            url      = settings.SALT_API['url'],
            username = settings.SALT_API['user'],
            password = settings.SALT_API['password']
        )
        
        sapi_glb = SaltAPI(
            url      = settings.SALT_API['url_glb'],
            username = settings.SALT_API['user'],
            password = settings.SALT_API['password']
        )
        minionsup, minionsdown= sapi.MinionStatus()
        minionsup_glb, minionsdown_glb= sapi_glb.MinionStatus()
        minionsdown_glb = [id for id in minionsdown_glb if 'SC' in id]
    else:
        minionsdown = []
        minionsdown_glb = []
    if len(minionsdown) != 0:
        send_mail(get_mail_list('check_salt_minion'),'Attention: salt_minion','Minion Down:'+ '\n\t' +'\n\t'.join(minionsdown))
    if len(minionsdown_glb) != 0:
        send_mail(admin_mail_addr,'Attention: 市场部服务器故障','Minion Down:'+ '\n\t' +'\n\t'.join(minionsdown_glb))
    end_time['check_salt_minion'] = time()

if __name__ == '__main__':
    start_time = time()
    end_time = multiprocessing.Manager().dict()
    #if not check_server_status():
    #    mail_content = (
    #        "-------------------------------------------------\n"
    #        "检测时间: %s\n"
    #        "检测服务: %s\n"
    #        "检测状态: %s\n"
    #        "-------------------------------------------------\n"
    #        )%(time(), server, '失败')
    #    os.system('nohup python %s/manage.py runserver 0.0.0.0:5000 &' %basedir)
    #    #send_mail(admin_mail_addr, 'Attention: django_server is down!', mail_content)
    #    mail_content = mail_content + (
    #        "尝试重启服务......\n"
    #        "重启时间: %s\n"
    #        )%time()
    #    sleep(4)
    #    if not check_server_status():
    #        mail_content = mail_content + (
    #            "检测状态: 失败\n"
    #            "-------------------------------------------------"
    #            )
    #        send_mail(admin_mail_addr, 'Attention: django_server is down!', mail_content)
    #        logger.error('%s %s 服务起不来！' %(time(), server))
    #    else:
    #        mail_content = mail_content + (
    #            "检测状态: 成功\n"
    #            "-------------------------------------------------"
    #            )
    #        send_mail(admin_mail_addr, 'Attention: django_server restarted!', mail_content)
    #        logger.error('%s %s 服务起不来！' %(time(), server))

    #multiprocessing three processes
    #pw_list = []
    #pw1 = multiprocessing.Process(target=check_services_fun, args=())
    #pw_list.append(pw1)
    #pw2 = multiprocessing.Process(target=check_salt_minion_fun, args=())
    #pw_list.append(pw2)
    #pw3 = multiprocessing.Process(target=check_salt_intrm, args=())
    #pw_list.append(pw3)
    #for pw in pw_list: pw.start()
    #for pw in pw_list: pw.join()
    check_services_fun()
    print "start_time:                 " + ColorP("%s" %start_time,                    fore = 'green') 
    print "check_services_end_time:    " + ColorP("%s" %end_time['check_services'],    fore = 'yellow')  
    #print "check_salt_minion_end_time: " + ColorP("%s" %end_time['check_salt_minion'], fore = 'yellow')  
    #print "check_salt_intrm_time:      " + ColorP("%s" %end_time['check_salt_intrm'],  fore = 'yellow')  
    print "end_time:                   " + ColorP("%s" %time(),                        fore = 'green')
