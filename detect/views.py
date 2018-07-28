#-_- coding: utf-8 -_-
from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponse
from django.views.decorators.csrf   import csrf_exempt, csrf_protect
from dwebsocket                     import require_websocket, accept_websocket
from models                         import domains
from monitor.models                 import telegram_ssl_alert_t
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
    domain_dict = {'domain':[], 'alert':{'default':None, 'others':[]}}

    if request.method == 'POST':
        try:
            product  = json.loads(request.body)['product']
            if str(product).lower() == 'all':
                domain_l = domains.objects.filter(status=1).all()
            else:
                domain_l = domains.objects.filter(status=1, product=product).all()

            alert_l  = telegram_ssl_alert_t.objects.filter(status=1).all()
        except Exception, e:
            logger.error(e.message)
            domain_l = []
            alert_l  = []

        for alert in alert_l:
            tmp_dict = {
                'name': alert.name,
                'chat_group': [ group.group for group in alert.chat_group.all() ],
                'user':       [ user.user for user in alert.user_id.all() ],
                'product':  (alert.product, alert.get_product_display()),
                'customer': (alert.customer, alert.get_customer_display()),
                'ex_one_m':  "",
                'ex_half_y': "",
                'failed':    "",
            }
            if tmp_dict['name'] == "默认":
                domain_dict['alert']['default']=tmp_dict
            else:
                domain_dict['alert']['others'].append(tmp_dict)

        for domain in domain_l:
            tmp_dict = {}
            tmp_dict['name']     = domain.name
            tmp_dict['product']  = (domain.product, domain.get_product_display())
            tmp_dict['customer'] = (domain.customer, domain.get_customer_display())
            tmp_dict['client']   = domain.group.client
            tmp_dict['method']   = domain.group.method
            tmp_dict['ssl']      = domain.group.ssl
            tmp_dict['retry']    = domain.group.retry
            domain_dict['domain'].append(tmp_dict)
        return HttpResponse(json.dumps(domain_dict))
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
            return HttpResponse(content='telegram 发送失败，参数错误！', status=502)
    else:
        return HttpResponse(status=403)