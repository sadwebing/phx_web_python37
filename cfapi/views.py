# coding: utf8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from dwebsocket import require_websocket
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from cf_api import CfApi
import json, logging, requests, re, datetime
logger = logging.getLogger('django')

@csrf_exempt 
def UpdateRecord(request):
    if request.method == 'POST':
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
            logger.info('update sccessfully!')
            return HttpResponse(json.dumps(result['result']))

    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')
