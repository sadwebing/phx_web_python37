# coding: utf8
from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from dwebsocket                     import require_websocket, accept_websocket
from django.views.decorators.csrf   import csrf_exempt, csrf_protect
from models                         import dnspod_account, domain_info, alter_history
from dnspod_api                     import DpApi
from accounts.views                 import HasDnsPermission, HasPermission, getIp, insert_ah
from phxweb.settings                import DnsPod_URL
from pypinyin                       import lazy_pinyin
import json, logging, requests, re, datetime
logger = logging.getLogger('django')

def takeId(elem):
    return elem['product_py']

@csrf_exempt
def GetDnspodProductRecords(request):
    if request.method == 'GET':
        return HttpResponse('You get nothing!')
    elif request.method == 'POST':
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
        logger.info('[POST]%s is requesting. %s' %(clientip, request.get_full_path()))

        if request.user.userprofile.manage == 1:
            products = dnspod_account.objects.all()
        else:
            products = [ dns.dnspod_account for dns in request.user.userprofile.dns.filter(permission='read').all() if dns.dnspod_account ]

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
                        'product':    product.name,
                        'product_py': lazy_pinyin(product.name),
                        'domain':     result['domains'],
                    })
        zone_name_list.sort(key=takeId) #以product 拼音排序
        return HttpResponse(json.dumps(zone_name_list))
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def GetDnspodZoneRecords(request):
    if request.method == 'GET':
        return HttpResponse('You get nothing!')
    elif request.method == 'POST':
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

        logger.info('[POST]%s is requesting. %s' %(clientip, request.get_full_path()))
        data = json.loads(request.body)['postdata']

        record_list = []
        for zone in data:
            dp_acc = dnspod_account.objects.get(name=zone['product'])

            try:
                dpapi = DpApi(DnsPod_URL, dp_acc.key)
            except Exception, e:
                logger.error("查询 %s 域名失败！%s" %(zone['name'], str(e)))
                return HttpResponseServerError("查询 %s 域名失败！" %zone['name'])
            else:
                result, status = dpapi.GetZoneRecords(zone['name'])
                if not status:
                    logger.error("查询 %s 域名失败！%s" %(zone['name'], str(result)))
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
def CreateDnspodRecords(request):
    if request.method == 'POST':
        clientip = getIp(request)
        username = request.user.username
        try:
            role = request.user.userprofile.role
        except:
            role = 'none'
        if not username:
            logger.info('user: 用户名未知 | [POST]%s is requesting. %s' %(clientip, request.get_full_path()))
            return HttpResponseServerError("用户名未知！")
            
        logger.info('user:%s | [POST]%s is requesting. %s' %(username, clientip, request.get_full_path()))
        data = json.loads(request.body)

        #判断是否有权限
        if not HasDnsPermission(request, "dnspod", data['product'], "add"):
            return HttpResponseServerError("抱歉，您没有新增账号[%s]解析的权限！" %data['product'])

        for sub_domain in data['sub_domain']:
            dp_acc = dnspod_account.objects.get(name=data['product'])
            record_name = data['zone'] if sub_domain == '@' else sub_domain+"."+data['zone']

            try:
                dpapi = DpApi(DnsPod_URL, dp_acc.key)
            except Exception, e:
                info = "新增 %s 域名失败！" %record_name
                logger.error(info)
                insert_ah(clientip, username, 
                        "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %('null', 'null', 'null', 'null'), 
                        "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(data['type'], record_name, data['value'], '1'), 
                        False, 'add')

                return HttpResponseServerError(info)
            else:
                result, status = dpapi.CreateZoneRecord(
                    domain         = data['zone'],
                    sub_domain     = sub_domain,
                    record_type    = data['type'],
                    value          = data['value'],
                    record_line    = data['record_line'],
                    #status         = 'enable' if data['enabled'] == '1' else 'disable',
                )
                
                if not status:
                    insert_ah(clientip, username, 
                        "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %('null', 'null', 'null', 'null'), 
                        "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(data['type'], sub_domain+'.'+data['zone'], data['value'], '1'), 
                        status, 'add')
                    return HttpResponseServerError('error!')
            insert_ah(clientip, username, 
                "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %('null', 'null', 'null', 'null'), 
                "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(data['type'], sub_domain+'.'+data['zone'], data['value'], '1'), 
                status, 'add')
        return HttpResponse(json.dumps(result))

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

            #判断是否有权限
            if not HasDnsPermission(request, "dnspod", data['product'], "add"):
                request.websocket.send('noPermission')
                ### close websocket ###
                request.websocket.close()
                break

            step = 0

            for sub_domain in data['sub_domain']:
                step += 1
                return_info           = {}
                return_info['domain'] = sub_domain+'.'+data['zone'] if sub_domain != "@" else data['zone']
                return_info['step']   = step
                dp_acc = dnspod_account.objects.get(name=data['product'])
                try:
                    dpapi = DpApi(DnsPod_URL, dp_acc.key)
                except Exception, e:
                    logger.error("新增 %s 域名失败！" %return_info['domain'])
                    return_info['result'] = False
                else:
                    result, status = dpapi.CreateZoneRecord(
                        domain         = data['zone'],
                        sub_domain     = sub_domain,
                        record_type    = data['type'],
                        value          = data['value'],
                        record_line    = data['record_line'],
                        #status         = 'enable' if data['enabled'] == '1' else 'disable',
                    )
                
                    if not status:
                        return_info['result'] = False
                    else:
                        return_info['result'] = True

                        insert_ah(clientip, username, 
                            "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %('null', 'null', 'null', 'null'), 
                            "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(data['type'], return_info['domain'], data['value'], '1'), 
                            status, 'add')

                request.websocket.send(json.dumps(return_info))
            ### close websocket ###
            request.websocket.close()

    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
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
            #判断是否有权限
            if not HasDnsPermission(request, "dnspod", record['product'], "change"):
                return HttpResponseServerError("抱歉，您没有修改账号[%s]解析的权限！" %record['product'])

            try:
                dpapi = DpApi(DnsPod_URL, dp_acc.key)
            except Exception, e:
                logger.error("修改 %s 域名失败！" %record['name'])
                insert_ah(clientip, username, 
                        "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %('null', 'null', 'null', 'null'), 
                        "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(record['type'], record['name'], record['value'], record['enabled']), 
                        False)
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
                    insert_ah(clientip, username, 
                            "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %('null', 'null', 'null', 'null'), 
                            "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(record['type'], record['name'], record['value'], record['enabled']), 
                            status)
                    return HttpResponseServerError('error!')

        return HttpResponse(result)
        insert_ah(clientip, username, 
                "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %('null', 'null', 'null', 'null'), 
                "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(record['type'], record['name'], record['value'], record['enabled']), 
                status)

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
                return_info['permission'] = True

                #判断是否有权限
                if not HasDnsPermission(request, "dnspod", record['product'], "change"):
                    return_info['permission']   = False
                    return_info['result'] = False
                    request.websocket.send(json.dumps(return_info))
                    continue

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

                insert_ah(clientip, username, 
                        "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(record['type'], record['name'], record['value'], record['enabled']), 
                        "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(data['type'], record['name'], data['value'], data['enabled']), 
                        return_info['result'])

                request.websocket.send(json.dumps(return_info))
            ### close websocket ###
            request.websocket.close()

    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def DeleteDnspodRecords(request):
    if request.method == 'GET':
        return HttpResponse('You get nothing!')
    elif request.method == 'POST':
        clientip = getIp(request)
        username = request.user.username
        manage   = request.user.userprofile.manage
        try:
            role = request.user.userprofile.role
        except:
            role = 'none'

        if not username:
            logger.info('user: 用户名未知 | [POST]%s is requesting. %s' %(clientip, request.get_full_path()))
            return HttpResponseServerError("用户名未知，请登陆有效账号！")

        #if username != 'phexus_sa':
        #    return HttpResponseServerError("抱歉，暂时不放开删除权限，请联系管理员！")
        #return HttpResponseServerError("抱歉，暂时不放开删除权限，请联系管理员！")

        logger.info('[POST]%s is requesting. %s' %(clientip, request.get_full_path()))
        data = json.loads(request.body)

        record_list = []
        for zone in data:
            if not HasDnsPermission(request, "dnspod", zone['product'], "delete"):
                return HttpResponseServerError("抱歉，您没有删除账号[%s]解析的权限！" %zone['product'])

            dp_acc = dnspod_account.objects.get(name=zone['product'])

            try:
                dpapi = DpApi(DnsPod_URL, dp_acc.key)
            except Exception, e:
                logger.error("删除 %s 域名失败！%s" %(zone['name'], str(e)))
                return HttpResponseServerError("删除 %s 域名失败！" %zone['name'])
            else:
                result, status = dpapi.DeleteZoneRecord(zone['zone'], zone['record_id'], zone['name'])
                if not status:
                    logger.error("删除 %s 域名失败！%s" %(zone['name'], str(result)))
                    return HttpResponseServerError("删除 %s 域名失败！" %zone['name'])
                else:
                    logger.info("删除 %s 域名成功！%s" %(zone['name'], str(result)))
                    insert_ah(clientip, username, 
                        "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(zone['type'], zone['name'], zone['value'], zone['enabled']), 
                        "null", 
                        status, 'delete')

        return HttpResponse("删除 %s 域名成功！" %zone['name'])
    else:
        return HttpResponse('nothing!')
        
