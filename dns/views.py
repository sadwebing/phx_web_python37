# coding: utf8
from django.shortcuts import render
from django.http      import HttpResponse, HttpResponseForbidden
from dwebsocket       import require_websocket
from models           import cf_account, dnspod_account
from cf_api           import CfApi
from dnspod           import *
from cf               import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf   import csrf_exempt, csrf_protect

import json, logging, requests, re, datetime
logger = logging.getLogger('django')

@csrf_exempt 
def UpdateRecord(request):
    if request.method == 'POST':
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            clientip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            clientip = request.META['REMOTE_ADDR']
        data = json.loads(request.body)

        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))
        api = CfApi('https://api.cloudflare.com/client/v4/zones/', 'lebo.technical001@gmail.com', '763d1ef590cea5ec364ddd6e676eee0e72f3d')
        result = api.UpdateDnsRecords(data['zone_id'], data['record_type'], data['record_name'], data['record_content'], data['proxied'])
        if result['result'] == 'id null':
            logger.info('%s doesn\'t exist. pls check!' %data['record_name'])
            return HttpResponse('%s doesn\'t exist. pls check!' %data['record_name'])
        elif result['result'] == 'id id more than one':
            logger.info('%s has more than one id. pls check!' %data['record_name'])
            return HttpResponse('%s has more than one id. pls check!' %data['record_name'])
        elif result['result'] == None or result['result'] == 'bad arguments':
            logger.info('wrong arguments. pls check!')
            return HttpResponse('wrong arguments. pls check!')
        elif result['result'] == {}:
            logger.info('request https://api.cloudflare.com raise a exception. pls check!')
            return HttpResponse('request https://api.cloudflare.com raise a exception. pls check!')
        else:
            logger.info('update successfully!')
            return HttpResponse(json.dumps(result['result']))

    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_protect
@login_required
def Index(request):
    title = u'CloudFlare-主页'
    global username, role, clientip
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        clientip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        clientip = request.META['REMOTE_ADDR']
    logger.info('%s is requesting %s' %(clientip, request.get_full_path()))

    product_list = cf_account.objects.values_list("name").all().order_by("name")
    logger.info('%s %s' %(type(product_list), product_list))

    return render(
        request,
        'dns/cloudflare_index.html',
        {
            'title': title,
            'clientip':clientip,
            'role': role,
            'username': username,
            'product_list': [name[0] for name in product_list],
        }
    )

@csrf_protect
@login_required
def DndpodIndex(request):
    title = u'DnsPod-主页'
    global username, role, clientip
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        clientip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        clientip = request.META['REMOTE_ADDR']
    logger.info('%s is requesting %s' %(clientip, request.get_full_path()))

    product_list = dnspod_account.objects.values_list("name").all().order_by("name")
    logger.info('%s %s' %(type(product_list), product_list))

    return render(
        request,
        'dns/dnspod_index.html',
        {
            'title': title,
            'clientip':clientip,
            'role': role,
            'username': username,
            'product_list': [name[0] for name in product_list],
        }
    )