#!/usr/bin/env python
#-_- coding:utf-8 -_-
#author: Arno
#introduciton:
#    监控HTTPS域名证书是否到期
#version: 2018/05/10 实现基本功能

import os, sys, datetime, logging, ssl, socket, threading, requests, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phxweb.settings")
from phxweb import settings
logging.basicConfig(level=logging.INFO, filename="check_ssl.log", format='%(asctime)s - %(levelname)s - %(message)s')
from ssl import SSLError

#获取当前目录
current_dir = os.path.abspath(os.path.dirname(__file__))

#telegram 参数
message = {} # 信息主体
message['doc']        = False
message['bot']        = "sa_monitor_bot" #AuraAlertBot: 大魔王
message['text']       = ""
message['group']      = 'arno_test' #domain_renew: 域名续费|证书续费
message['parse_mode'] = "HTML"
message['doc_file']   = 'message.txt'

#django接口
dj_url = 'sa.l510881.com'

#一个月，半年，一年到期的时间
d_one_y      = datetime.datetime.now()  + datetime.timedelta(365)
d_half_y     = datetime.datetime.now()  + datetime.timedelta(182)
d_one_m      = datetime.datetime.now()  + datetime.timedelta(31)
ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
timeout      = 10

#telegram 通知
def sendTelegram(message):
    #telegram 通知
    try:
        ret = requests.post('http://%s/detect/send_telegram' %dj_url, data=json.dumps(message))
    except Exception as e:
        print (str(e))

#获取域名
def getDomains(product='all'):
    try:
        ret = requests.post('http://%s/detect/get_domains' %dj_url, headers={'Content-Type': 'application/json'}, data=json.dumps({'product': product}))
    except Exception as e:
        print (str(e))
        return []
    else:
        return ret.json()
        
class sslExpiry(object):
    def __init__(self, domain):
        '''
            获取https域名证书到期的时间，以及是否是有效证书
        '''
        self.__domain = domain
    
    def setConn(self, bundle=None):
        '''
            初始化https连接
        '''
    
        if bundle:
            context = ssl.create_default_context(cafile="%s/bundle/%s" %(current_dir, bundle))
        else:
            context = ssl.create_default_context()
        context.verify_mode = ssl.CERT_REQUIRED
        conn    = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=self.__domain,
            #do_handshake_on_connect=False,
        )
        conn.settimeout(timeout)
        return conn
        
    def getCert(self):
        #bundles = os.listdir(u'%s/bundle/' %current_dir).insert(0, None)
        bundles = os.listdir(u'%s/bundle/' %current_dir)
        bundles.insert(0, None)
        index = 0
        ssl   = False
        while not ssl:
            print index
            conn = self.setConn(bundle=bundles[index])
            try:
                conn.connect((self.__domain, 443))
            except SSLError:
                index += 1
                if index < len(bundles):
                    continue
                else:
                    logging.error('%s 443 ssl error' %(self.__domain))
                    return SSLError
            except Exception, e:
                logging.error('%s 443 connection error: \n %s' %(self.__domain, e))
                return False
            else:
                ssl = True
                ssl_info = conn.getpeercert()
            #return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
        return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
    
class myThread(threading.Thread):
    def __init__(self,domain):
        super().__init__()
        self.__domain = domain
    #def exePool(domain):
    def run(self):
        cert = sslExpiry(self.__domain).getCert()
        self.t  = None
        if not cert:
            self.t = (False, "连接失败")
        elif cert == SSLError:
            self.t = (False, "证书不合法")
        else:
            self.t = (True, cert)

    def get_result(self):
        return self.t
    
if __name__ == "__main__":
    #print sslExpiry('alcp33.com').getTime()
    li = []
    print getDomains(product=13)
    sys.exit()
    for domain in getDomains(product='ali'):
        t = myThread(domain)
        li.append(t)
        t.start()
    for t in li:
        t.join()
        print t.get_result()
    