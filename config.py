#-_- coding: utf-8 -_-

import multiprocessing

#配置文件
#bind = "0.0.0.0:8000"

#开发模式
reload = False

workers = multiprocessing.cpu_count() * 2 + 1    #进程数
threads = 4 #指定每个进程开启的线程数

accesslog = "./logs/access.log"
loglevel  = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
