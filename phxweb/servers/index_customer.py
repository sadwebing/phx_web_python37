# coding: utf8
from monitor.models    import project_t, minion_t, minion_ip_t
from accounts.views    import HasPermission, HasServerPermission, getIp, getProjects
from phxweb            import settings
from detect.telegram   import sendTelegram
from saltstack.command import Command
from phxweb.customer   import DefConsumer
from servers.views     import encryptPasswd

import json, logging, re, datetime, rsa, base64

logger = logging.getLogger('django')

#telegram 参数
message = settings.message_TEST

class ServersUpdate(DefConsumer):
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
            return_info['info']   = ""
            return_info['permission'] = True
            return_info['result']     = True

            #判断是否有权限
            if not HasServerPermission(self.message, record, "change"):
                return_info['permission'] = False
                return_info['result']     = False
                self.message.reply_channel.send({'text': json.dumps(return_info)})
                ### close websocket ###
                self.close()
                break

            #修改密码
            cmd    = 'echo "%s" |passwd root --stdin' %data['password'].replace('`', '\`') # `这个符号在Linux命令行有特殊含义，需要转义
            result = Command(record['minion_id'], 'cmd.run', cmd, 'glob').CmdRun()[record['minion_id']]

            if 'all authentication tokens updated successfully' not in result:
                return_info['result'] = False
                return_info['info']   = result
                self.message.reply_channel.send({'text': json.dumps(return_info)})
                continue

            #密码加密并存放
            crypto, status = encryptPasswd(data['password'], record)
            if not status:
                return_info['result'] = False
                return_info['info']   = "密码修改成功，但是密码加密失败：" + result
                message['text']       = "@arno\r\n" + return_info['info']
                sendTelegram(message).send()
                self.message.reply_channel.send({'text': json.dumps(return_info)})
                continue
            try:
                update = minion_t.objects.get(minion_id=record['minion_id'])
                update.password = crypto
                update.save()
            except Exception, e:
                sendTelegram(message).send()
                return_info['result'] = False
                return_info['info']   = "密码修改成功，但是密码存入失败：" + str(e)
                message['text']       = "@arno\r\n" + return_info['info']
                sendTelegram(message).send()
                self.message.reply_channel.send({'text': json.dumps(return_info)})
                continue

            self.message.reply_channel.send({'text': json.dumps(return_info)})
        self.close()