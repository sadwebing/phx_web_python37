#!/usr/bin/env python
#-_- coding:utf-8 -_-
#author: Arno
#introduciton:
#    监控HTTPS域名证书是否到期
#version: 2018/06/12 实现基本功能
#         2018/07/26 域名区分产品和客户, 信息长度大于4096，以文件形式发送信息
#         2018/07/29 域名区分产品和客户, 发送到相应的客户群组

import os, sys, datetime, logging, ssl, socket, threading, requests, json, urlparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phxweb.settings")
from phxweb import settings
from ssl import SSLError, CertificateError

#获取当前目录
current_dir = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(level=logging.INFO, filename="%s/check_ssl.log" %current_dir, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#telegram 参数
message = {} # 信息主体
message['doc']        = False
message['bot']        = "sa_monitor_bot" #AuraAlertBot: 大魔王
message['text']       = ""
message['group']      = 'domain_renew' #domain_renew: 域名续费|证书续费
message['parse_mode'] = "HTML"
message['doc_name']   = 'message.txt'

#django接口
#dj_url = 'sa.l510881.com'
dj_url = '127.0.0.1:5000'

#一个月，半年，一年到期的时间
d_one_y      = datetime.datetime.now() + datetime.timedelta(365)
d_half_y     = datetime.datetime.now() + datetime.timedelta(182)
d_one_m      = datetime.datetime.now() + datetime.timedelta(31)
ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
nor_date_fmt = r'%Y/%m/%d %H:%M:%S'
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
            #print index
            conn = self.setConn(bundle=bundles[index])
            try:
                conn.connect((self.__domain, 443))
            except (SSLError, CertificateError):
                index += 1
                if index < len(bundles):
                    continue
                else:
                    logger.error('%s 443 ssl error' %(self.__domain))
                    return SSLError
            except Exception, e:
                logger.error('%s 443 connection error: \n %s' %(self.__domain, e))
                return e
            else:
                ssl = True
                ssl_info = conn.getpeercert()
            #return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
        return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
    
class myThread(threading.Thread):
    def __init__(self,domain_l):
        super(myThread, self).__init__()
        self.__domain_l = domain_l
        self.__domain   = urlparse.urlsplit(domain_l['name']).netloc.split(':')[0].strip()
        
    def run(self):
        self.t = None
        
        ssle = sslExpiry(self.__domain)

        for i in range(self.__domain_l['retry']):
            cert = ssle.getCert()
            #print cert
            if isinstance(cert, datetime.datetime):
                break

        if cert == SSLError:
            self.t = (False, self.__domain_l, u"证书不合法")
        elif not isinstance(cert, datetime.datetime):
            self.t = (False, self.__domain_l, cert)
        else:
            self.t = (True,  self.__domain_l, cert)

    def get_result(self):
        return self.t
    
if __name__ == "__main__":
    #print sslExpiry('alcp33.com').getTime()
    li = []
    #print getDomains(product=7); sys.exit()

    failed    = ""
    ex_half_y = ""
    ex_one_m  = ""
    
    getDomainsDict = getDomains(product='all')

    for domain_l in getDomainsDict['domain']:
        if domain_l['customer'][0] in [14, 15]:  #['大象6668[dx_6668]', '大象70887[dx_70887]']
            continue
        scheme = urlparse.urlsplit(domain_l['name']).scheme

        if scheme == "https":
            t = myThread(domain_l)
            li.append(t)
            t.start()

    for t in li:
        t.join()
        result = t.get_result()

        alert = None
        #将结果存入报警列表
        for tmp in getDomainsDict['alert']['others']:
            if result[1]['product'][0] == tmp['product'][0] and result[1]['customer'][0] == tmp['customer'][0]:
                alert = tmp
                break
            else:
                continue
        if not alert:
            alert = getDomainsDict['alert']['default']

        customer = "_"+result[1]['customer'][1] if result[1]['customer'][0] != 29 else ""
        info     = "["+result[1]['product'][1]+customer+"]"+urlparse.urlsplit(result[1]['name']).netloc.split(':')[0].strip()
        if result[0]:
            if d_one_m > result[2]:
                alert['ex_one_m'] += result[2].strftime(nor_date_fmt) + ": " + info + "\r\n"
            elif d_half_y > result[2]:
                alert['ex_half_y'] += result[2].strftime(nor_date_fmt) + ": " + info + "\r\n"
        else:
            alert['failed'] += str(result[2]) + ": " + info + "\r\n"

    getDomainsDict['alert']['others'].append(getDomainsDict['alert']['default'])

    for alert in getDomainsDict['alert']['others']:
        message['text']    = ""
        message['doc']     = False
        message['caption'] = ""

        if alert['failed']:
            message['text'] += u"<pre>检测失败的域名: </pre>\r\n" + alert['failed']
        if alert['ex_one_m']:
            message['text'] += u"<pre>一个月内证书到期域名: </pre>\r\n" + alert['ex_one_m']

        for group in alert['chat_group']:
            message['group'] = group
            if message['text']:
                if len(message['text']) >= 4096:
                    message['text']    = message['text'].replace('\r\n', '\n')
                    message['doc']     = True
                    message['caption'] = u"\r\n%s 请提醒客户更换证书！" %" ".join([ "@"+user for user in alert['user'] ]) if len(alert['user']) !=0 else ""
                else:
                    message['text'] += u"\r\n%s 请提醒客户更换证书！" %" ".join([ "@"+user for user in alert['user'] ]) if len(alert['user']) !=0 else ""
                sendTelegram(message)
    