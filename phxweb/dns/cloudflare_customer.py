# coding: utf8
from dns.models      import cf_account, domain_info, alter_history
from dns.cf_api      import CfApi
from accounts.views  import HasDnsPermission, HasPermission, getIp, insert_ah
from phxweb.settings import CF_URL
from phxweb.customer import DefConsumer

import json, logging

logger = logging.getLogger('django')

class DnsCloudflareRecordUpdate(DefConsumer):
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
            if not HasDnsPermission(self.message, "cf", record['product'], "change"):
                return_info['permission'] = False
                return_info['result'] = False
                self.message.reply_channel.send({'text': json.dumps(return_info)})
                continue

            cf_acc = cf_account.objects.filter(name=record['product']).first()
            cfapi  = CfApi(CF_URL, cf_acc.email, cf_acc.key)
            if data['proxied'] == 'true':
                proxied = True
            else:
                proxied = False

            result = cfapi.UpdateZoneRecord(record['zone_id'], data['type'], record['name'], data['content'], proxied=proxied, record_id=record['record_id'])
            if not result['success']:
                return_info['result'] = False
            else:
                return_info['result'] = True
            logger.info("req_ip: %s | user: %s | updaterecord: { 'type':%s, 'name': %s, 'content': %s, 'proxied':%s } ---> { 'type':%s, 'name': %s, 'content': %s, 'proxied':%s }" %(self.clientip, self.username, record['type'], record['name'], record['content'], record['proxied'], data['type'], record['name'], data['content'], proxied))

            insert_ah(self.clientip, self.username, 
                    "'type':%s, 'name': %s, 'content': %s, 'proxied':%s" %(record['type'], record['name'], record['content'], record['proxied']),
                    "'type':%s, 'name': %s, 'content': %s, 'proxied':%s" %(data['type'], record['name'], data['content'], proxied),
                    return_info['result'])

            self.message.reply_channel.send({'text': json.dumps(return_info)})

class DnsCloudflareRecordAdd(DefConsumer):
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
            cf_acc = cf_account.objects.get(name=data['product'])
            try:
                cfapi = CfApi(CF_URL, cf_acc.email, cf_acc.key)
            except Exception, e:
                logger.error("新增 %s 域名失败！" %return_info['domain'])
                return_info['result'] = False
            else:
                result = cfapi.CreateZoneRecord(
                    zone_id        = data['zone_id'],
                    record_name    = return_info['domain'],
                    record_type    = data['type'],
                    record_content = data['content'],
                    proxied        = True if data['proxied'].lower() == 'true' else False,
                )
            
                return_info['result'] = result['success']

                if return_info['result']:
                    insert_ah(self.clientip, self.username, 
                        "null", 
                        "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(data['type'], sub_domain+'.'+data['zone'], data['content'], '1'), 
                        return_info['result'], 'add')

            self.message.reply_channel.send({'text': json.dumps(return_info)})