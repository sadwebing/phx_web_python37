#!/usr/bin/env python
#-_- coding:utf-8 -_-
#author: Arno


import os, sys, datetime, logging, ssl, socket

#获取当前目录
current_dir = os.path.abspath(os.path.dirname(__file__))

#声明协议类型,同事生成socket连接对象
client = socket.socket()