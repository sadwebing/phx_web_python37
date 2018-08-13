#!/usr/bin/python3
#-_- coding:utf-8 -_-
#introduciton:
#    监控主站域名是否能够访问
#version: 2018/05/10 实现基本功能
#         2018/05/12 多线程执行
#         2018/05/16 使用自建接口发送telegram信息
#         2018/05/17 优化报警信息
#         2018/05/22 multiprocessing--->threading 优化线程
#         2018/05/26 故障域名循环检测，避免一时的网络问题导致误报
#         2018/06/29 域名分产品报警
#         2018/07/26 域名区分产品和客户，信息长度大于4096，以文件形式发送信息

import re,os,sys,requests,datetime,multiprocessing,json,threading
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from bs4        import BeautifulSoup
from time       import sleep
#from color_print import ColorP
from socket     import gethostname, gethostbyname
from subprocess import getoutput

sys.setrecursionlimit(1000000)

# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

__author__ = 'Arno'

#获取当前脚本路径
basedir = os.path.abspath(os.path.dirname(__file__))

#requests参数
requests.adapters.DEFAULT_RETRIES = 3
error_status = 'null'

#telegram 参数
message = {} # 信息主体
message['group'] = 'domain_alert' #domain_alert
message['bot']   = 'sa_monitor_bot'
message['text']  = ""
message['doc']   = False
message['doc_name'] = "warning.txt"

#获取当前时间，以特定的格式，如Wed, 09 May 2018 12:51:25 GMT
def getDate():
    return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S   GMT')

#telegram 通知
def sendTelegram(message):
    try:
        ret = requests.post('http://sa.l510881.com/detect/send_telegram', data=json.dumps(message))
    except Exception as e:
        print (str(e))

#获取html的title
def getHtmlTitle(html):
    html = BeautifulSoup(html,'html.parser')
    try:
        return html.title.text
    except:
        return None

#获取域名
def getDomains(product='all'):
    try:
        ret = requests.post('http://sa.l510881.com/detect/get_domains', headers={'Content-Type': 'application/json'}, data=json.dumps({'product': product}))
    except Exception as e:
        print (str(e))
        return []
    else:
        return ret.json()

#执行检测域名请求
class ReqDomains(object):
    def __init__(self, domain):
        self.__url      = ''
        self.__name     = ''
        self.__product  = ''
        self.__customer = ''
        self.__method   = 'head'
        self.__verify   = False
        self.__timeout  = 10
        self.__retry    = 3
        self.__reg      = '^.*[a-zA-Z0-9]+.*\.[a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$'
        self.__headers  = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
        if isinstance(domain, dict):
            if ('client' in domain.keys()) and domain['client'] == 'wap': self.__headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}
            if 'method' in domain.keys(): self.__method = domain['method']
            #if ('ssl' in domain.keys()) and domain['ssl'] != 1: self.__verify = False
            if 'timeout' in domain.keys(): self.__timeout = domain['timeout']
            if 'product' in domain.keys(): self.__product = domain['product'][1]
            if 'customer' in domain.keys(): self.__customer = domain['customer'][1]
            if 'name' in domain.keys() and len(domain['name'].split('/')) >= 3: 
                self.__name = domain['name'].split('/')[2].split(':')[0].strip()
                #print (self.__name)
                self.__url  = domain['name'].strip()
        elif isinstance(domain, str) and len(domain.split('/')) >= 3: 
            self.__name = domain.split('/')[2].split(':')[0].strip()
            self.__url  = domain.strip()

        #获取域名解析地址
        try:
            self.__ip = gethostbyname(self.__name)
            #print (self.__ip)
        except:
            self.__ip = None

    def IsNameVaild(self):
        '''判断域名是否有效'''
        #return True if re.fullmatch(self.__reg, self.__name) else False
        return True if re.search(self.__reg, self.__name) else False

    def IsIpVaild(self):
        '''获取域名解析地址'''
        return True if self.__ip else False

    def ExeReq(self):
        '''执行域名检测'''
        res = []
        s   = requests.Session()
        req = requests.Request(
                method  = self.__method.strip(), 
                url     = self.__url.strip(), 
                headers = self.__headers
            ).prepare()
        try:
            ret = s.send(req, verify=self.__verify, timeout=self.__timeout)
        except requests.exceptions.ConnectTimeout:
            res.append({error_status: {self.__ip:'连接超时！'}})
        except requests.exceptions.ReadTimeout:
            res.append({error_status: {self.__ip:'加载超时！'}})
        except requests.exceptions.SSLError:
            res.append({error_status: {self.__ip:'证书认证错误！'}})
        #except requests.exceptions.NewConnectionError:
        #    res.append({error_status: {self.__ip:'找不到主机名！'}})
        except requests.exceptions.MissingSchema:
            res.append({error_status: {self.__ip:'协议头无效！'}})
        except requests.exceptions.ConnectionError:
            res.append({error_status: {self.__ip:'连接错误！'}})
        except Exception as e:
            res.append({error_status: {self.__ip:e}})
        else:
            if len(ret.history) != 0:
                for r in ret.history:
                    res.append({r.status_code: r.url})
            res.append({ret.status_code: ret.url})
            res.append({'title': getHtmlTitle(ret.content)})
        return res

class myThread(threading.Thread):
    def __init__(self,domain):
        super().__init__()
        self.domain=domain
    #def exePool(domain):
    def run(self):
        rd = ReqDomains(self.domain)
        self.__product  = rd.__dict__['_ReqDomains__product']
        self.__customer = rd.__dict__['_ReqDomains__customer']
        self.t  = None
        
        for i in range(rd.__dict__['_ReqDomains__retry']):
            if not rd.IsNameVaild() or not rd.IsIpVaild():
                #print (self.domain)
                continue

        if not rd.IsNameVaild():
            self.t = ": ".join([self.__product + "_" +self.__customer, rd.__dict__['_ReqDomains__url'], '域名无效.'])
            print (self.t)
        elif not rd.IsIpVaild():
            self.t = ": ".join([self.__product + "_" +self.__customer, rd.__dict__['_ReqDomains__url'], '域名解析无效.'])
            print (self.t)
        else:
            for i in range(rd.__dict__['_ReqDomains__retry']):
                res = rd.ExeReq()
                print (self.__product + "_" +self.__customer, rd.__dict__['_ReqDomains__url'], str(res))
                #print ('.', end='')
                if error_status not in res[0].keys() and 200 in res[-2].keys():
                    break
                sleep(2)
            if error_status in res[0].keys():
                self.t = ": ".join([self.__product + "_" +self.__customer, rd.__dict__['_ReqDomains__url'], str(res[0][error_status])])
            elif 200 not in res[-2].keys():
                self.t = ": ".join([self.__product + "_" +self.__customer, rd.__dict__['_ReqDomains__url'], str(res)])

    def get_result(self):
        if self.t:
            return [self.__product + "_" +self.__customer, self.t]
        else:
            return None

def getIp():
    try:
        ret = requests.get('http://myip.ipip.net')
    except Exception as e:
        print ('获取当前IP失败......')
        print (str(e))
        ip = gethostname()
    else:
        if ret.status_code == 200:
            ip = ret.text
        else:
            ip = gethostname()
    return ip

def sendAlert(ip, results):
    java      = ""
    ruiying   = ""
    fenghuang = ""
    for result in results:
        if result[0] == "java":
            java += '\r\n' + result[1]
        elif result[0] == "ruiying":
            ruiying += '\r\n' + result[1]
        else:
            fenghuang += '\r\n' + result[1]
    if java:
        if len(java) >= 4096:
            message['doc'] = True
        message['text'] = ip + java
        message['group'] = 'java_domain'
        sendTelegram(message)
    if ruiying:
        if len(ruiying) >= 4096:
            message['doc'] = True
        message['text'] = ip + ruiying
        message['group'] = 'ruiying_domain'
        sendTelegram(message)
    if fenghuang:
        if len(fenghuang) >= 4096:
            message['doc'] = True
        message['text'] = ip + fenghuang
        message['group'] = 'domain_alert' #domain_alert
        sendTelegram(message)
        
if __name__ == '__main__':
    ip = getoutput('curl -s http://ip.cn')
    li = []
    results = []

    for domain in getDomains(product='all')['domain']:
        t = myThread(domain)
        li.append(t)
        t.start()
    for t in li:
        t.join()
        if t.get_result(): results.append(t.get_result())

    sendAlert(ip, results)
