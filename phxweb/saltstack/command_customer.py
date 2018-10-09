# coding: utf8
from phxweb.customer   import DefConsumer
from phxweb            import settings
from saltstack.saltapi import SaltAPI
from monitor.models    import project_t, minion_t, minion_ip_t
from saltstack.command import Command
from accounts.limit    import LimitAccess
from accounts.views    import getIp, getProjects
from accounts.models   import user_project_authority_t
from saltstack.reflesh import *

import json, logging, time
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

logger = logging.getLogger('django')

#telegram 参数
message = settings.message_ONLINE

class SaltstackCommandDeploy(DefConsumer):
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

        ### step one ###
        info = {}
        info['step'] = 'one'
        info['project'] = data['project']
        info['minion_id'] = data['minion_id']
        self.message.reply_channel.send({'text': json.dumps(info)})

        ### final step ###
        info = {}
        info['step'] = 'final'

        commandexe = Command(data['minion_id'], 'state.sls', expr_form='list')
        info['results'] = commandexe.StateSls('nginx.conf_dev')
        #info['results'] = commandexe.StateSls('nginx.reload')
        #info['results'] = dict(info['results'], **commandexe.StateSls('nginx.reload'))

        self.message.reply_channel.send({'text': json.dumps(info)})
        self.close()

class SaltstackCommandExecute(DefConsumer):
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
        ### final step ###
        info = {}
        info['step'] = 'final'
        arglist = ["runas=%s" %data['exe_user']]
        arglist.append(data['arguments'])
        commandexe = Command(data['target'], data['function'], arglist, data['expr_form'],)
        if data['function'] == 'test.ping':
            info['results'] = commandexe.TestPing()
        elif data['function'] == 'cmd.run':
            info['results'] = commandexe.CmdRun()
        elif data['function'] == 'state.sls':
            info['results'] = commandexe.StateSls(data['arguments'])

        self.message.reply_channel.send({'text': json.dumps(info)})
        self.close()