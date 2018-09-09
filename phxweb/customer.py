# coding: utf8
from channels          import Channel, Group
from channels.sessions import channel_session
from channels.auth     import channel_session_user, channel_session_user_from_http
from channels.generic.websockets import WebsocketConsumer

import json, logging

logger = logging.getLogger('django')

class DefConsumer(WebsocketConsumer):

    http_user_and_session = True

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ["test"]

    def connect(self, message, **kwargs):
        """
        在连接阶段accept: True用于接受连接，close: True用于拒绝连接
        """
        self.message.reply_channel.send({"accept": True})

        self.clientip = '127.0.0.1'
        self.username = self.message.user.username
        try:
            self.role = self.message.user.userprofile.role
        except:
            self.role = 'none'

        if self.username == "":
            logger.info('user: 用户名未知 | [websocket]%s is requesting. %s' %(self.clientip, self.message['path']))
            self.message.reply_channel.send({'text': 'userNone'})
            self.message.reply_channel.send({"close": True})
            return False
        logger.info('user: %s | [websocket]%s is requesting. %s' %(self.username, self.clientip, self.message['path']))

    def args(self):
        return self

    def receive(self, text=None, bytes=None, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        pass
        
    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        pass