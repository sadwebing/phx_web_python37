#!/usr/bin/env python
#-_- coding:utf-8 -_-
#author: Arno
#update: 2018/01/27 add check_services and get_result
#        2018/01/28 add ColorT

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
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
server = 'http://103.99.62.71:5000/'
requests.adapters.DEFAULT_RETRIES = 3
logger = logging.getLogger('django')
error_status = 'null'
code_list = ['200', '301', '302', '303', '405']
rewrite_list = ['301', '302', '303']
normal_list = ['200']


class ColorT(object):
    def __init__(self, product, project, server_type, domain, url):
        self.__product     = product
        self.__project     = project
        self.__server_type = server_type
        self.__domain      = domain
        self.__url         = url

    def content_p(self, code, fore='red'):
        if fore == 'white':
            content = str(code) + "\t" + '_'.join([self.__product, self.__project, self.__server_type]) + "[%s]:  "%self.__domain +  self.__url + '\n'
        else:
            content = ColorP(str(code), fore = fore) + "\t" + '_'.join([self.__product, self.__project, self.__server_type]) + "[%s]:  "%self.__domain +  self.__url + '\n'
        return content

def get_result(result, project_info, content_body):
    color_t = ColorT(project_info.product, project_info.project, project_info.server_type, project_info.domain, result['url'])
    try:
        ret = requests.head(result['url'], headers={'Host': result['domain']}, timeout=16)
        code = str(ret.status_code)
        if code not in code_list:
            content_body += color_t.content_p(code, fore='white')
            content = color_t.content_p(code)
        else:
            if code in rewrite_list:
                content = color_t.content_p(code, fore='white')
                url = ret.headers['Location'].replace(project_info.domain, result['ip'])
                color_t = ColorT(project_info.product, project_info.project, project_info.server_type, project_info.domain, url)
                try:
                    ret_r = requests.head(url, headers={'Host': project_info.domain}, verify=False, timeout=16)
                    #print ret.headers['Location']
                    code = str(ret_r.status_code)
                    if code not in code_list:
                        content_body += content + color_t.content_p(code, fore='white')
                        content = content + color_t.content_p(code)
                    else:
                        content = content + color_t.content_p(code, fore='white')
                except:
                    result['code'] = error_status
                    result['info'] = '失败'
                    content_body += content + color_t.content_p(result['code'], fore='white')
                    content = content + color_t.content_p(result['code'])
            elif code in normal_list:
                content = color_t.content_p(code, fore='white')
    except:
        result['code'] = error_status
        result['info'] = '失败'
        content_body += color_t.content_p(result['code'], fore='white')
        content = color_t.content_p(result['code'])

    print content,

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
            result['ip']  = minion.ip_addr
            result['url'] = 'http://' + minion.ip_addr + project_info.uri

            if len(result['url']) == 0:
                continue

            content_body = pool.apply_async(get_result, (result, project_info, content_body, )).get()
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
