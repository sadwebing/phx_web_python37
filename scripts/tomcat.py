#!/usr/bin/env python
#-_- coding:utf-8 -_-
#author: Arno
#update: 2017/07/07 add multiprocessing pool
#        2017/07/11 optimize send_mail
#        2017/07/13 update check app server
#        2017/07/22 add color print

import re,os,sys,smtplib,requests,datetime,logging,multiprocessing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from time import sleep
#from saltstack.command import Command
from email.mime.text import MIMEText
from email.header import Header
reload(sys)
sys.setdefaultencoding('utf8')
import django,json
os.environ['DJANGO_SETTINGS_MODULE'] = 'phxweb.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phxweb.settings")
#django.setup()
from monitor.models import project_t, minion_t
from color_print import ColorP

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
server = 'http://103.99.62.71:5000/'
requests.adapters.DEFAULT_RETRIES = 3
logger = logging.getLogger('django')
error_status = 'null'

def get_result(result, project_info, code_list, content_body):
    try:
        ret = requests.head(result['url'], headers={'Host': result['domain']}, timeout=16)
        if project_info.project =='ALL_TSD_WS' and ret.status_code == 500:
            result['code'] = '200'
        else:
            result['code'] = '%s' %ret.status_code
        try:
            title = re.search('<title>.*?</title>', ret.content)
            result['info'] = title.group().replace('<title>', '').replace('</title>', '')
        except AttributeError:
            if result['code'] in code_list:
                result['info'] = '正常'
            else:
                result['info'] = '失败'
    except:
        result['code'] = error_status
        result['info'] = '失败'

    if result['code'] not in code_list:
        content = ColorP(result['code'], fore = 'red') + "\t" + '_'.join([result['product'], result['project'], result['server_type']]) + ":  " +  result['url']
        #content_body = content_body + "<tr style=\"font-size:15px\"><td >%s</td><td >%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" %(result['access_time'],result['product'] , result['project'], result['server_type'], result['domain'], result['url'], result['code'], result['info'])
        content_body = content_body + '\n' + result['code'] + "\t" + '_'.join([result['product'], result['project'], result['server_type']]) + "[%s]:  " %project_info.domain +  result['url']
    else:
        content = result['code'] + "\t" + '_'.join([result['product'], result['project'], result['server_type']]) + ":  " +  result['url']
    print content

    #logger.info(MIMEText(str(result), 'utf-8'))
    return content_body

def check_services():
    content_head = """\
    <html><head><title>HTML email</title></head><body>
    <style>
        .table_css table {
            text-align:center;
            width:1500px;
            border: solid #dddddd;
            border-collapse:collapse;
            border-radius: 4px;
        }
        .table_css table th {
            border: 1px solid #dddddd;
        }
        .table_css table td {
            border: 1px solid #dddddd;
        }
    </style>
    <div class=\"table_css\">
    <table>
    <tr style=\"font-size:14px\">
    <th style="width:120px;">时间</th> 
    <th style="width:120px;">产品</th> 
    <th style="width:120px;">工程</th> 
    <th style="width:120px;">服务类型</th> 
    <th style="width:120px;">域名</th> 
    <th style="width:300px;">路径</th> 
    <th style="width:120px;">状态</th> 
    <th style="width:300px;">备注</th>
    </tr>
    """
    content_body = ""
    content = ""
    pool = multiprocessing.Pool(processes=25)
    project_all = project_t.objects.filter(status=1).all()
    code_list = ['200', '302', '303', '405']
    for project_info in project_all:
        global result
        result = {}
        result['access_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        result['product'] = project_info.product
        result['project'] = project_info.project
        result['domain'] = project_info.domain
        result['server_type'] = project_info.server_type
        minion_all = minion_t.objects.filter(minion_id=project_info.minion_id, status=1).all()
        for minion in minion_all:
            result['url'] = 'http://' + minion.ip_addr + project_info.uri

            if len(result['url']) == 0:
                continue

            content_body = pool.apply_async(get_result, (result, project_info, code_list, content_body, )).get()
        #result['code'], result['info'] = get_result(result, project_info, code_list)
        
        #if content_body != "":
        #    content = content_head + content_body + "</table></div></body></html>"
    pool.close()
    pool.join()
    return content_body

def time():
    current_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    return current_time

def check_server_status():
    try:
        ret = requests.get(server,timeout=2)
        record = server_status(access_time=time(), url=server, status=ret.status_code, info=ret.text)
        record.save()
        logger.info('%s is running.' %server)
        return True
    except requests.exceptions.ConnectionError:
        record = server_status(access_time=time(), url=server, status=error_status, info='null')
        record.save()
        logger.error('%s check failed.' %server)
        return False

if __name__ == '__main__':
    print "使用check.py"
