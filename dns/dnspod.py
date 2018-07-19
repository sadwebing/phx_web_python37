# coding: utf8
from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from dwebsocket                     import require_websocket, accept_websocket
from django.views.decorators.csrf   import csrf_exempt, csrf_protect
from models                         import dnspod_account, domain_info, alter_history
from dnspod_api                     import DpApi
from accounts.views                 import HasPermission, getIp
from phxweb.settings                import DnsPod_URL
import json, logging, requests, re, datetime
logger = logging.getLogger('django')

@csrf_exempt
def GetDnspodProductRecords(request):
    if request.method == 'GET':
        return HttpResponse('You get nothing!')
    elif request.method == 'POST':
        clientip = getIp(request)
        logger.info('[POST]%s is requesting. %s' %(clientip, request.get_full_path()))

        products = dnspod_account.objects.all()
        zone_name_list = []
        for product in products:
            try:
                dpapi  = DpApi(DnsPod_URL, product.key)
            except Exception, e:
                logger.error("查询 %s 账号失败！" %product.name)
                return HttpResponseServerError("查询 %s 账号失败！" %product.name)
            else:
                result, status = dpapi.GetDnsLists(type='all')
                if not status:
                    return HttpResponseServerError('error!')
                else:
                    zone_name_list.append({
                        'product': product.name,
                        'domain' : result['domains'],
                    })
        return HttpResponse(json.dumps(zone_name_list))
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def GetDnspodZoneRecords(request):
    if request.method == 'GET':
        return HttpResponse('You get nothing!')
    elif request.method == 'POST':
        clientip = getIp(request)
        logger.info('[POST]%s is requesting. %s' %(clientip, request.get_full_path()))
        data = json.loads(request.body)['postdata']
        logger.info(data)
        record_list = []
        for zone in data:
            dp_acc = dnspod_account.objects.get(name=zone['product'])

            try:
                dpapi = DpApi(DnsPod_URL, dp_acc.key)
            except Exception, e:
                logger.error("查询 %s 域名失败！" %zone['name'])
                return HttpResponseServerError("查询 %s 域名失败！" %zone['name'])
            else:
                result, status = dpapi.GetZoneRecords(zone['name'])
                if not status:
                    return HttpResponseServerError('error!')
                else:
                    for record in result['records']:
                        if record['type'] in ['A', 'CNAME']:
                            record_list.append({
                                'product':        zone['product'],
                                'zone':           zone['name'],
                                'zone_id':        zone['id'],
                                'sub_domain':     record['name'],
                                'name':           record['name']+'.'+zone['name'] if record['name'] != '@' else zone['name'],
                                'type':           record['type'],
                                'value':          record['value'],
                                'record_id':      record['id'],
                                'record_line':    record['line'],
                                'record_line_id': record['line_id'],
                                #'record_line_id': record['line_id'].replace('=', '%3D'),
                                'enabled':        record['enabled'],
                            })

        return HttpResponse(json.dumps(record_list))
    else:
        return HttpResponse('nothing!')
        
@accept_websocket
@csrf_exempt
def UpdateDnspodRecords(request):
    if request.method == 'POST':
        clientip = getIp(request)
        username = request.user.username
        try:
            role = request.user.userprofile.role
        except:
            role = 'none'
        if not username:
            request.websocket.send('userNone')
            logger.info('user: 用户名未知 | [POST]%s is requesting. %s' %(clientip, request.get_full_path()))
            return HttpResponseServerError("用户名未知！")
            
        logger.info('user:%s | [POST]%s is requesting. %s' %(username, clientip, request.get_full_path()))
        data = json.loads(request.body)
        logger.info(data)

        for record in data:
            dp_acc = dnspod_account.objects.get(name=record['product'])

            try:
                dpapi = DpApi(DnsPod_URL, dp_acc.key)
            except Exception, e:
                logger.error("修改 %s 域名失败！" %record['name'])
                insert_ah(clientip, username, 'null', 'null', 'null', 'null', record['type'], record['name'], record['value'], record['enabled'], str(False))
                return HttpResponseServerError("修改 %s 域名失败！" %record['name'])
            else:
                result, status = dpapi.UpdateZoneRecord(
                    domain         = record['zone'],
                    record_id      = record['record_id'],
                    sub_domain     = record['sub_domain'],
                    record_type    = record['type'],
                    value          = record['value'],
                    record_line_id = record['record_line_id'],
                    status         = 'enable' if record['enabled'] == '1' else 'disable',
                )
                
                if not status:
                    insert_ah(clientip, username, 'null', 'null', 'null', 'null', record['type'], record['name'], record['value'], record['enabled'], str(False))
                    return HttpResponseServerError('error!')
        insert_ah(clientip, username, 'null', 'null', 'null', 'null', record['type'], record['name'], record['value'], record['enabled'], str(True))
        return HttpResponse(result)

    elif request.is_websocket():
        clientip = getIp(request)
        username = request.user.username
        try:
            role = request.user.userprofile.role
        except:
            role = 'none'
        if not username:
            request.websocket.send('userNone')
            logger.info('user: 用户名未知 | [WS]%s is requesting. %s' %(clientip, request.get_full_path()))
            ### close websocket ###
            request.websocket.close()

        logger.info('user:%s | [WS]%s is requesting. %s' %(username, clientip, request.get_full_path()))
        for postdata in request.websocket:
            if not postdata:
                ### close websocket ###
                request.websocket.close()
                break
            data = json.loads(postdata)
            step = 0

            for record in data['records']:
                step += 1
                return_info           = {}
                return_info['record'] = record
                return_info['step']   = step
                dp_acc = dnspod_account.objects.get(name=record['product'])
                try:
                    dpapi = DpApi(DnsPod_URL, dp_acc.key)
                except Exception, e:
                    logger.error("修改 %s 域名失败！" %record['name'])
                    return_info['result'] = False
                else:
                    result, status = dpapi.UpdateZoneRecord(
                        domain         = record['zone'],
                        record_id      = record['record_id'],
                        sub_domain     = record['sub_domain'],
                        record_type    = data['type'],
                        value          = data['value'],
                        record_line_id = record['record_line_id'],
                        status         = 'enable' if data['enabled'] == '1' else 'disable',
                    )
                
                    if not status:
                        return_info['result'] = False
                    else:
                        return_info['result'] = True

                insert_ah(clientip, username, record['type'], record['name'], record['value'], record['enabled'], data['type'], record['name'], data['value'], data['enabled'], str(return_info['result']))

                request.websocket.send(json.dumps(return_info))
            ### close websocket ###
            request.websocket.close()

    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

def insert_ah(clientip, username, type_before, name_before, value_before, status_before, type_after, name_after, value_after, status_after, result):
    logger.info("req_ip: %s | user: %s | updaterecord: { 'type':%s, 'name': %s, 'content': %s, 'enabled':%s } ---> { 'type':%s, 'name': %s, 'content': %s, 'enabled':%s } {result: %s}" %(clientip, username, type_before, name_before, value_before, status_before, type_after, name_after, value_after, status_after, result))

    insert_h = alter_history(
            time    = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            req_ip  = clientip,
            user    = username,
            pre_rec = "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(type_before, name_before, value_before, status_before),
            now_rec = "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(type_after, name_after, value_after, status_after),
            status  = result,
        )

    insert_h.save()