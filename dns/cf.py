# coding: utf8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from dwebsocket import require_websocket
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from models import cf_account, domain_info
from cf_api import CfApi
from accounts.views import HasPermission
from phxweb.settings import CF_URL
import json, logging, requests, re, datetime
logger = logging.getLogger('django')

@csrf_exempt
def GetProductRecords(request):
    if request.method == 'GET':
        return HttpResponse('You get nothing!')
    elif request.method == 'POST':
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            clientip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            clientip = request.META['REMOTE_ADDR']
        logger.info('[POST]%s is requesting. %s' %(clientip, request.get_full_path()))
        data = json.loads(request.body)
        zone_name_list = []
        for name in data['product']:
            cf_acc = cf_account.objects.filter(name=name).first()
            cfapi = CfApi(CF_URL, cf_acc.email, cf_acc.key)
            page = 1
            result = cfapi.GetDnsLists(page=page)
            total_pages = result['result_info']['total_pages']
            if len(result['result']) == 0:
                continue
            while page <= total_pages:
                for record in result['result']:
                    tmp_dict = {}
                    tmp_dict['name'] = record['name']
                    tmp_dict['id'] = record['id']
                    tmp_dict['product'] = name
                    zone_name_list.append(tmp_dict)
                page += 1
                result = cfapi.GetDnsLists(page=page)

        return HttpResponse(json.dumps(zone_name_list))
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def GetZoneRecords(request):
    if request.method == 'GET':
        return HttpResponse('You get nothing!')
    elif request.method == 'POST':
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            clientip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            clientip = request.META['REMOTE_ADDR']
        logger.info('[POST]%s is requesting. %s' %(clientip, request.get_full_path()))
        data = json.loads(request.body)['postdata']
        logger.info(data)
        record_list = []
        for zone in data:
            cf_acc = cf_account.objects.filter(name=zone['product']).first()
            cfapi = CfApi(CF_URL, cf_acc.email, cf_acc.key)
            result = cfapi.GetZoneRecords(zone['zone_id'])
            if len(result['result']) == 0:
                continue
            for record in result['result']:
                tmp_dict = {}
                tmp_dict['product'] = zone['product']
                tmp_dict['zone'] = record['zone_name']
                tmp_dict['name'] = record['name']
                tmp_dict['type'] = record['type']
                tmp_dict['content'] = record['content']
                tmp_dict['proxied'] = record['proxied']
                tmp_dict['record_id'] = record['id']
                tmp_dict['zone_id'] = record['zone_id']
                record_list.append(tmp_dict)

        return HttpResponse(json.dumps(record_list))
    else:
        return HttpResponse('nothing!')

@require_websocket
@csrf_exempt
def UpdateRecords(request):
    if request.is_websocket():
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
        logger.info('user:%s | [POST]%s is requesting. %s' %(username, clientip, request.get_full_path()))
        for postdata in request.websocket:
            #logger.info(type(postdata))
            data = json.loads(postdata)
            step = 0

            for record in data['records']:
                step += 1
                return_info = {}
                return_info['record'] = record
                return_info['step'] = step
                cf_acc = cf_account.objects.filter(name=record['product']).first()
                cfapi = CfApi(CF_URL, cf_acc.email, cf_acc.key)
                if data['proxied'] == 'true':
                    proxied = True
                else:
                    proxied = False

                result = cfapi.UpdateDnsRecords(record['zone_id'], data['type'], record['name'], data['content'], proxied=proxied, record_id=record['record_id'])
                if not result['success']:
                    return_info['result'] = False
                else:
                    return_info['result'] = True
                logger.info("req_ip: %s | user: %s | updaterecord: { 'type':%s, 'name': %s, 'content': %s, 'proxied':%s }" %(clientip, username, data['type'], record['name'], data['content'], proxied))
                request.websocket.send(json.dumps(return_info))

        ### close websocket ###
        request.websocket.close()

@csrf_exempt
def UpdateApiRoute(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        data = json.loads(request.body)
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))

        domain_l = domain_info.objects.filter(domain=data['domain']).all()
        zone_id = domain_l[0].zone_id
        record_id = domain_l[0].record_id
        cf_account_name = domain_l[0].cf_account_name
        return_info = {}
        r_type = 'CNAME'

        cf_acc = cf_account.objects.filter(name=cf_account_name).first()
        cfapi = CfApi(CF_URL, cf_acc.email, cf_acc.key)

        if data['route'] == 'cloudflare':
            proxied = True
        else:
            proxied = False

        if data['route'] == 'nginx':
            content = [domain_i.content for domain_i in domain_l if domain_i.route == 'nginx' ]
        elif data['route'] == 'cloudflare':
            content = [domain_i.content for domain_i in domain_l if domain_i.route == 'cloudflare' ]
        elif data['route'] == 'aegins':
            content = [domain_i.content for domain_i in domain_l if domain_i.route == 'aegins' ]
        elif data['route'] == 'wangsu':
            content = [domain_i.content for domain_i in domain_l if domain_i.route == 'wangsu' ]

        result = cfapi.UpdateDnsRecords(zone_id, r_type, data['domain'], content[0], proxied=proxied, record_id=record_id)

        #logger.info(result)

        if not result['success']:
            return_info['result'] = False
            logger.error(result)
        else:
            return_info['result'] = True
            #api_list = domain_info.objects.filter(domain=data['domain'], status=1).all()
            api_list = domain_info.objects.filter(domain=data['domain']).all()
            for info in api_list:
                if info.route == data['route']:
                    info.route_status = 1
                    info.save()
                else:
                    info.route_status = 0
                    info.save()

        #logger.info(return_info)
        return HttpResponse(json.dumps(return_info))

@csrf_exempt
def GetApiRoute(request):
    if request.method == 'GET' or request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        data = json.loads(request.body)
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))

        return_info = []
        #api_list = domain_info.objects.filter(product=data['product'], status=1).all()
        api_list = domain_info.objects.filter(product=data['product']).all()
        for info in api_list:
            temp = {}
            temp['product'] = info.product
            temp['client'] = info.client
            temp['domain'] = info.domain
            temp['content'] = info.content
            temp['route_status'] = info.route_status
            temp['route'] = info.route
            return_info.append(temp)
        return HttpResponse(json.dumps(return_info))