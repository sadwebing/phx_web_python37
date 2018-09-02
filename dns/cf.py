# coding: utf8
from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from dwebsocket                     import require_websocket, accept_websocket
from django.views.decorators.csrf   import csrf_exempt, csrf_protect
from models                         import cf_account, domain_info, alter_history
from cf_api                         import CfApi
from accounts.views                 import HasDnsPermission, HasPermission, getIp, insert_ah
from phxweb.settings                import CF_URL
from pypinyin                       import lazy_pinyin
import json, logging, requests, re, datetime
logger = logging.getLogger('django')

def takeId(elem):
    return elem['product_py']

@csrf_exempt
def GetProductRecords(request):
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

        if request.user.is_superuser:
            products = cf_account.objects.all()
        else:
            products = [ dns.cf_account for dns in request.user.userprofile.dns.filter(permission='read').all() if dns.cf_account ]

        zone_name_list = []

        for product in products:
            cf_acc      = cf_account.objects.get(name=product.name)
            cfapi       = CfApi(CF_URL, cf_acc.email, cf_acc.key)
            page        = 1
            result      = cfapi.GetDnsLists(page=page)
            total_pages = result['result_info']['total_pages']
            tmp_dict = {
                'product':    product.name,
                'product_py': lazy_pinyin(product.name),
                'domain':     [],
                }
            if len(result['result']) == 0:
                continue
            while page <= total_pages:
                for record in result['result']:
                    tmp_dict['domain'].append({
                            'name': record['name'],
                            'id':   record['id'],
                            'status': 'enable',
                        })
                page += 1
                result = cfapi.GetDnsLists(page=page)
            zone_name_list.append(tmp_dict)

        #logger.info(zone_name_list)
        zone_name_list.sort(key=takeId) #以product 拼音排序
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
            cfapi  = CfApi(CF_URL, cf_acc.email, cf_acc.key)
            result = cfapi.GetZoneRecords(zone['zone_id'])
            if len(result['result']) == 0:
                continue
            for record in result['result']:
                tmp_dict = {}
                tmp_dict['product']   = zone['product']
                tmp_dict['zone']      = record['zone_name']
                tmp_dict['name']      = record['name']
                tmp_dict['type']      = record['type']
                tmp_dict['content']   = record['content']
                tmp_dict['proxied']   = record['proxied']
                tmp_dict['record_id'] = record['id']
                tmp_dict['zone_id']   = record['zone_id']
                record_list.append(tmp_dict)

        return HttpResponse(json.dumps(record_list))
    else:
        return HttpResponse('nothing!')

@accept_websocket
@csrf_exempt
def CreateRecords(request):
    if request.method == 'POST':
        clientip = getIp(request)
        username = request.user.username
        try:
            role = request.user.userprofile.role
        except:
            role = 'none'
        #if not username:
        #    logger.info('user: 用户名未知 | [POST]%s is requesting. %s' %(clientip, request.get_full_path()))
        #    return HttpResponseServerError("用户名未知！")

        logger.info('user:%s | [POST]%s is requesting. %s' %(username, clientip, request.get_full_path()))
        data = json.loads(request.body)

        #判断是否有权限
        #if not HasDnsPermission(request, "cf", data['product'], "add"):
        #    return HttpResponseServerError("抱歉，您没有新增账号[%s]解析的权限！" %data['product'])

        result_list = []
        for sub_domain in data['sub_domain']:
            cf_acc = cf_account.objects.get(name=data['product'])
            record_name = sub_domain+'.'+data['zone'] if sub_domain != '@' else data['zone']

            try:
                cfapi = CfApi(CF_URL, cf_acc.email, cf_acc.key)
            except Exception, e:
                info  = "新增 %s 域名失败: %s" %(record_name, str(e))
                logger.error(info)
                result = {'result': None, 'errors': str(e), 'success': False}
            else:
                result = cfapi.CreateZoneRecord(
                    zone_id        = data['zone_id'],
                    record_name    = record_name,
                    record_type    = data['type'],
                    record_content = data['content'],
                    proxied        = True if data['proxied'].lower() == 'true' else False,
                )
            result_list.append(result)

            insert_ah(clientip, username, 
                    "null", 
                    "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(data['type'], record_name, data['content'], '1'), 
                    result['success'], 'add')

            if not result['success']:
                return HttpResponseServerError(result_list)
        return HttpResponse(json.dumps(result_list))

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
            if not HasDnsPermission(request, "cf", data['product'], "add"):
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
                cf_acc = cf_account.objects.get(name=data['product'])
                try:
                    cfapi = CfApi(CF_URL, cf_acc.email, cf_acc.key)
                except Exception, e:
                    logger.error("新增 %s 域名失败！" %return_info['domain'])
                    return_info['result'] = False
                else:
                    result = cfapi.CreateZoneRecord(
                        zone_id        = data['zone_id'],
                        record_name    = return_info['domain'],
                        record_type    = data['type'],
                        record_content = data['content'],
                        proxied        = True if data['proxied'].lower() == 'true' else False,
                    )
                
                    return_info['result'] = result['success']

                insert_ah(clientip, username, 
                    "null", 
                    "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(data['type'], sub_domain+'.'+data['zone'], data['content'], '1'), 
                    return_info['result'], 'add')

                request.websocket.send(json.dumps(return_info))

            ### close websocket ###
            request.websocket.close()

    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@require_websocket
@csrf_exempt
def UpdateRecords(request):
    if request.is_websocket():
        global username, role, clientip
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            clientip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            clientip = request.META['REMOTE_ADDR']
        username = request.user.username
        try:
            role = request.user.userprofile.role
        except:
            role = 'none'
        if not username:
            request.websocket.send('userNone')
            logger.info('user: 用户名未知 | [POST]%s is requesting. %s' %(clientip, request.get_full_path()))
            ### close websocket ###
            request.websocket.close()

        logger.info('user:%s | [POST]%s is requesting. %s' %(username, clientip, request.get_full_path()))
        for postdata in request.websocket:
            #logger.info(type(postdata))
            if not postdata:
                logger.info('this is test!')
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
                if not HasDnsPermission(request, "cf", record['product'], "change"):
                    return_info['permission']   = False
                    return_info['result'] = False
                    request.websocket.send(json.dumps(return_info))
                    continue

                cf_acc = cf_account.objects.filter(name=record['product']).first()
                cfapi  = CfApi(CF_URL, cf_acc.email, cf_acc.key)
                if data['proxied'] == 'true':
                    proxied = True
                else:
                    proxied = False

                result = cfapi.UpdateZoneRecord(record['zone_id'], data['type'], record['name'], data['content'], proxied=proxied, record_id=record['record_id'])
                if not result['success']:
                    return_info['result'] = False
                else:
                    return_info['result'] = True
                logger.info("req_ip: %s | user: %s | updaterecord: { 'type':%s, 'name': %s, 'content': %s, 'proxied':%s } ---> { 'type':%s, 'name': %s, 'content': %s, 'proxied':%s }" %(clientip, username, record['type'], record['name'], record['content'], record['proxied'], data['type'], record['name'], data['content'], proxied))

                insert_h = alter_history(
                        time    = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        req_ip  = clientip,
                        user    = username,
                        pre_rec = "'type':%s, 'name': %s, 'content': %s, 'proxied':%s" %(record['type'], record['name'], record['content'], record['proxied']),
                        now_rec = "'type':%s, 'name': %s, 'content': %s, 'proxied':%s" %(data['type'], record['name'], data['content'], proxied)
                    )

                insert_h.save()

                request.websocket.send(json.dumps(return_info))

            ### close websocket ###
            request.websocket.close()

@csrf_exempt
def DeleteRecords(request):
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

        logger.info('[POST]%s is requesting. %s' %(clientip, request.get_full_path()))
        data = json.loads(request.body)

        record_list = []
        for zone in data:
            if not HasDnsPermission(request, "cf", zone['product'], "delete"):
                return HttpResponseServerError("抱歉，您没有删除账号[%s]解析的权限！" %zone['product'])

            cf_acc = cf_account.objects.get(name=zone['product'])

            try:
                cfapi  = CfApi(CF_URL, cf_acc.email, cf_acc.key)
            except Exception, e:
                logger.error("删除 %s 域名失败！%s" %(zone['name'], str(e)))
                return HttpResponseServerError("删除 %s 域名失败！" %zone['name'])
            else:
                result = cfapi.DeleteZoneRecord(zone['zone_id'], zone['record_id'])
                if not result['success']:
                    logger.error("删除 %s 域名失败！%s" %(zone['name'], str(result)))
                    return HttpResponseServerError("删除 %s 域名失败！" %zone['name'])
                else:
                    logger.info("删除 %s 域名成功！%s" %(zone['name'], str(result)))
                    insert_ah(clientip, username, 
                        "'type':%s, 'name': %s, 'content': %s, 'enabled':%s" %(zone['type'], zone['name'], zone['content'], zone['proxied']), 
                        "null", 
                        result['success'], 'delete')

        return HttpResponse("删除 %s 域名成功！" %zone['name'])
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def UpdateApiRoute(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        data = json.loads(request.body)
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))

        domain_l        = domain_info.objects.filter(domain=data['domain']).all()
        zone_id         = domain_l[0].zone_id
        record_id       = domain_l[0].record_id
        cf_account_name = domain_l[0].cf_account_name
        return_info     = {}
        r_type          = 'CNAME'

        cf_acc = cf_account.objects.filter(name=cf_account_name).first()
        cfapi  = CfApi(CF_URL, cf_acc.email, cf_acc.key)

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

        result = cfapi.UpdateZoneRecord(zone_id, r_type, data['domain'], content[0], proxied=proxied, record_id=record_id)

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
        data     = json.loads(request.body)
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))

        return_info = []
        #api_list = domain_info.objects.filter(product=data['product'], status=1).all()
        api_list = domain_info.objects.filter(product=data['product']).all()
        for info in api_list:
            temp = {}
            temp['product']      = info.product
            temp['client']       = info.client
            temp['domain']       = info.domain
            temp['content']      = info.content
            temp['route_status'] = info.route_status
            temp['route']        = info.route
            return_info.append(temp)
        return HttpResponse(json.dumps(return_info))