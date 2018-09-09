# coding: utf8
from dns.models      import dnspod_account, domain_info, alter_history
from dns.dnspod_api  import DpApi
from accounts.views  import HasDnsPermission, HasPermission, getIp, insert_ah
from phxweb.settings import DnsPod_URL
from phxweb.customer import DefConsumer

import json, logging

logger = logging.getLogger('django')

class DnsDnspodRecordUpdate(DefConsumer):
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

        for record in data['records']:
            step += 1
            return_info           = {}
            return_info['record'] = record
            return_info['step']   = step
            return_info['permission'] = True

            #判断是否有权限
            if not HasDnsPermission(self.message, "dnspod", record['product'], "change"):
                return_info['permission'] = False
                return_info['result'] = False
                self.message.reply_channel.send({'text': json.dumps(return_info)})
                continue

            dp_acc = dnspod_account.objects.get(name=record['product'])
            try:
                dpapi = DpApi(DnsPod_URL, dp_acc.key)
            except Exception, e:
                logger.error("修改 %s 域名失败！" %record['name'])
                return_info['result'] = False
            else:
                result, status = dpapi.UpdateZoneRecord(
                    domain         = record['zone'],
                    record_id      = record['record_id'],
                    sub_domain     = record['sub_domain'],
                    record_type    = data['type'],
                    value          = data['value'],
                    record_line_id = record['record_line_id'],
                    status         = 'enable' if data['enabled'] == '1' else 'disable',
                )
                
                if not status:
                    return_info['result'] = False
                else:
                    return_info['result'] = True
            insert_ah(self.clientip, self.username, 
                    "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(record['type'], record['name'], record['value'], record['enabled']), 
                    "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(data['type'], record['name'], data['value'], data['enabled']), 
                    return_info['result'])

            self.message.reply_channel.send({'text': json.dumps(return_info)})

class DnsDnspodRecordAdd(DefConsumer):
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

        return_info = {}
        return_info['permission'] = True
        data = json.loads(self.message['text'])

        self.clientip = '127.0.0.1'
        self.username = self.message.user.username
        try:
            self.role = self.message.user.userprofile.role
        except:
            self.role = 'none'

        #判断是否有权限
        if not HasDnsPermission(self.message, "dnspod", data['product'], "add"):
            return_info['permission'] = False
            return_info['result'] = False
            self.message.reply_channel.send({'text': json.dumps(return_info)})
            self.close()

        step = 0

        for sub_domain in data['sub_domain']:
            step += 1
            return_info['domain'] = sub_domain+'.'+data['zone'] if sub_domain != "@" else data['zone']
            return_info['step']   = step
            dp_acc = dnspod_account.objects.get(name=data['product'])
            try:
                dpapi = DpApi(DnsPod_URL, dp_acc.key)
            except Exception, e:
                logger.error("新增 %s 域名失败！" %return_info['domain'])
                return_info['result'] = False
            else:
                result, status = dpapi.CreateZoneRecord(
                    domain         = data['zone'],
                    sub_domain     = sub_domain,
                    record_type    = data['type'],
                    value          = data['value'],
                    record_line    = data['record_line'],
                    #status         = 'enable' if data['enabled'] == '1' else 'disable',
                ) 
                
                if not status:
                    return_info['result'] = False
                else:
                    return_info['result'] = True

                    insert_ah(self.clientip, self.username, 
                        "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %('null', 'null', 'null', 'null'), 
                        "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(data['type'], return_info['domain'], data['value'], '1'), 
                        status, 'add')

            self.message.reply_channel.send({'text': json.dumps(return_info)})