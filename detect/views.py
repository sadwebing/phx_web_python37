#-_- coding: utf-8 -_-
from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponse
from django.views.decorators.csrf   import csrf_exempt, csrf_protect
from dwebsocket                     import require_websocket, accept_websocket
from models                         import domains
from accounts.limit                 import LimitAccess
from telegram                       import sendTelegram
from phxweb                         import settings
import json, logging, requests, re

logger = logging.getLogger('django')

@csrf_exempt
def GetDomains(request):
    title = u'获取检测域名'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        clientip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        clientip = request.META['REMOTE_ADDR']
    logger.info('%s is requesting %s' %(clientip, request.get_full_path()))
    domain_list = []

    if request.method == 'POST':
        try:
            product  = json.loads(request.body)['product']
            if str(product).lower() == 'all':
                domain_l = domains.objects.filter(status=1).all()
            else:
                domain_l = domains.objects.filter(status=1, product=product).all()
        except Exception, e:
            logger.error(e.message)
            domain_l = []

        for domain in domain_l:
            tmp_dict = {}
            tmp_dict['name']    = domain.name
            tmp_dict['product'] = domain.get_product_display()
            tmp_dict['client']  = domain.group.client
            tmp_dict['method']  = domain.group.method
            tmp_dict['ssl']     = domain.group.ssl
            tmp_dict['retry']   = domain.group.retry
            domain_list.append(tmp_dict)
        return HttpResponse(json.dumps(domain_list))
    else:
        return HttpResponse(status=403)

@csrf_exempt
def SendTelegram(request):
    title = u'发送telegram信息'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        clientip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        clientip = request.META['REMOTE_ADDR']
    logger.info('%s is requesting %s' %(clientip, request.get_full_path()))

    if request.method == 'POST':
        try:
            message = json.loads(request.body)
            if not isinstance(message, dict): 
                logger.error('%s is not dict.' %message)
                s = sendTelegram({'text': clientip + ': 发送telegram信息失败，参数不是字典！', 'bot': 'sa_monitor_bot', 'group': 'arno_test'}) #arno_test
                if s.send():
                    return HttpResponse(content='参数错误！', status=500)
                else: 
                    return HttpResponse(content='telegram 发送失败！', status=502)
        except Exception, e:
            logger.error(e.message)
            s = sendTelegram({'text': clientip + ': 发送telegram信息失败！\r\n' + e.message, 'bot': 'sa_monitor_bot', 'group': 'arno_test'}) #arno_test
            if s.send():
                return HttpResponse(content='参数错误！', status=500)
            else: 
                return HttpResponse(content='telegram 发送失败！', status=502)


        s = sendTelegram(message)
        if s.send():
            return HttpResponse('发送成功！')
        else: 
            return HttpResponse(content='telegram 发送失败！', status=502)
    else:
        return HttpResponse(status=403)