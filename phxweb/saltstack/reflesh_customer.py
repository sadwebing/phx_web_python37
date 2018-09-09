# coding: utf8
from phxweb.customer       import DefConsumer
from phxweb                import settings
from accounts.views        import getIp
from saltstack.tencent_api import tcApi
from saltstack.ws_api      import wsApi
from saltstack.reflesh     import sendTelegramRe
from detect.models         import domains
from monitor.models        import cdn_proj_t
from detect.models         import cdn_account_t as cdn_t
from detect.telegram       import sendTelegram

import json, logging, time, urlparse

logger = logging.getLogger('django')

#telegram 参数
message = settings.message_ONLINE

class SaltstackRefleshExecuteCdn(DefConsumer):
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True
    channel_session_user = True

    # Set to True if you want it, else leave it out
    strict_ordering = False

    def receive(self, text=None, bytes=None, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        #self.close()

        self.clientip = '127.0.0.1'
        self.username = self.message.user.username
        try:
            self.role = self.message.user.userprofile.role
        except:
            self.role = 'none'

        data = json.loads(self.message['text'])
        step = 0

        ### step one ##
        info = {}
        info['step'] = 'one'
        self.message.reply_channel.send({'text': json.dumps(info)})
        #time.sleep(2)
        ### two step ###
        info['step'] = 'two'
        cdn_d = {}
        cdn   = cdn_t.objects.get(id=data['id'])
        cdn_d[cdn.get_name_display()+"_"+cdn.account] = {
            'name': cdn.get_name_display(),
            'domain': data['domain'],
            'secretid': str(cdn.secretid),
            'secretkey': str(cdn.secretkey),
            'failed': [],
            'sccess': [],
        }

        #logger.info(cdn_d)
        for cdn in cdn_d:
            info['cdn'] = cdn
            if cdn_d[cdn]['domain']:
                #开始清缓存，判断CDN接口是否存在
                if cdn_d[cdn]['name'] == "tencent":
                    req = tcApi(cdn_d[cdn]['secretid'], cdn_d[cdn]['secretkey'])
                elif cdn_d[cdn]['name'] == "wangsu":
                    req = wsApi(cdn_d[cdn]['secretid'], cdn_d[cdn]['secretkey'])
                else:
                    info['result'] = ["CDN 接口不存在！"]
                    cdn_d[cdn]['failed'].append("%s: 接口不存在！" %cdn)
                    self.message.reply_channel.send({'text': json.dumps(info)})
                    continue

                while len(cdn_d[cdn]['domain']) != 0 :
                    domains_c            = cdn_d[cdn]['domain'][:10]
                    cdn_d[cdn]['domain'] = cdn_d[cdn]['domain'][10:]

                    for uri in data['uri']:
                        result, status = req.purge(domains_c, uri)
                        if status:
                            info['result'] = [ domain+uri+": 清缓存成功。" for domain in domains_c ]
                            cdn_d[cdn]['sccess'] += [ domain+uri for domain in domains_c ]
                        else:
                            info['result'] = [ domain+uri+": 清缓存失败！" for domain in domains_c ]
                            cdn_d[cdn]['failed'] += [ domain+uri for domain in domains_c ]
                        self.message.reply_channel.send({'text': json.dumps(info)})
        info['step'] = 'final'
        self.message.reply_channel.send({'text': json.dumps(info)})
        for cdn in cdn_d:
            if cdn_d[cdn]['failed']:
                message["text"] = cdn_d[cdn]['failed']
                message['caption'] = cdn + ': 域名缓存清理失败!'
                sendTelegramRe(message)
            if cdn_d[cdn]['sccess']:
                message["text"] = cdn_d[cdn]['sccess']
                message['caption'] = cdn + ': 域名缓存清理成功。'
                sendTelegramRe(message)
        self.close()

class SaltstackRefleshExecute(DefConsumer):
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True
    channel_session_user = True

    # Set to True if you want it, else leave it out
    strict_ordering = False

    def receive(self, text=None, bytes=None, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        #self.close()
        data = json.loads(self.message['text'])

        self.clientip = '127.0.0.1'
        self.username = self.message.user.username
        try:
            self.role = self.message.user.userprofile.role
        except:
            self.role = 'none'

        ### step one ##
        info = {}
        info['step'] = 'one'
        self.message.reply_channel.send({'text': json.dumps(info)})
        #time.sleep(2)
        ### two step ###
        info['step'] = 'two'
        cdn_d = {}
        cdns  = cdn_t.objects.all()
        for cdn in cdns:
            cdn_d[cdn.get_name_display()+"_"+cdn.account] = {
                'name': cdn.get_name_display(),
                'domain': [],
                'secretid': str(cdn.secretid),
                'secretkey': str(cdn.secretkey),
                'failed': [],
                'sccess': [],
            }

        domain_l = domains.objects.filter(id__in=data['domain']).all()
        logger.info(domain_l)
        for domain in domain_l:
            for cdn in domain.cdn.all():
                cdn_d[cdn.get_name_display()+"_"+cdn.account]['domain'].append(urlparse.urlsplit(domain.name).scheme+"://"+urlparse.urlsplit(domain.name).netloc)
        #logger.info(cdn_d)
        for cdn in cdn_d:
            info['cdn'] = cdn
            if cdn_d[cdn]['domain']:
                #开始清缓存，判断CDN接口是否存在
                if cdn_d[cdn]['name'] == "tencent":
                    req = tcApi(cdn_d[cdn]['secretid'], cdn_d[cdn]['secretkey'])
                elif cdn_d[cdn]['name'] == "wangsu":
                    req = wsApi(cdn_d[cdn]['secretid'], cdn_d[cdn]['secretkey'])
                else:
                    info['result'] = ["CDN 接口不存在！"]
                    cdn_d[cdn]['failed'].append("%s: 接口不存在！" %cdn)
                    self.message.reply_channel.send({'text': json.dumps(info)})
                    continue

                while len(cdn_d[cdn]['domain']) != 0 :
                    domains_c            = cdn_d[cdn]['domain'][:10]
                    cdn_d[cdn]['domain'] = cdn_d[cdn]['domain'][10:]

                    for uri in data['uri']:
                        result, status = req.purge(domains_c, uri)
                        if status:
                            info['result'] = [ domain+uri+": 清缓存成功。" for domain in domains_c ]
                            cdn_d[cdn]['sccess'] += [ domain+uri for domain in domains_c ]
                        else:
                            info['result'] = [ domain+uri+": 清缓存失败！" for domain in domains_c ]
                            cdn_d[cdn]['failed'] += [ domain+uri for domain in domains_c ]
                        self.message.reply_channel.send({'text': json.dumps(info)})
        info['step'] = 'final'
        self.message.reply_channel.send({'text': json.dumps(info)})
        for cdn in cdn_d:
            if cdn_d[cdn]['failed']:
                message["text"] = cdn_d[cdn]['failed']
                message['caption'] = cdn + ': 域名缓存清理失败!'
                sendTelegramRe(message)
            if cdn_d[cdn]['sccess']:
                message["text"] = cdn_d[cdn]['sccess']
                message['caption'] = cdn + ': 域名缓存清理成功。'
                sendTelegramRe(message)
        self.close()