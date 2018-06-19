# coding: utf8
from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponse, HttpResponseForbidden
from dwebsocket                     import require_websocket
from django.views.decorators.csrf   import csrf_exempt, csrf_protect
from models                         import project_t, minion_t
from detect.models                  import domains, groups
from saltstack.command              import Command
from accounts.views                 import HasPermission, getIp
from phxweb                         import settings
import json, logging, requests, re, datetime

logger = logging.getLogger('django')
error_status = 'null'

prod_d = {}
for line in settings.choices_prod:
    prod_d[line[1]] = line[0]

@csrf_exempt
def DomainsQuery(request):
    if request.method == 'GET':
        return HttpResponse('You get nothing!')
    elif request.method == 'POST':
        clientip = getIp(request)
        logger.info('[POST]%s is requesting. %s' %(clientip, request.get_full_path()))
        try:
            data   = json.loads(request.body)
            status = list(data['status']) if data.has_key('status') else None
            num    = int(data['num']) if data.has_key('num') and str(data['num']).lower() != 'all' else None
            group  = data['group'] if data.has_key('group') else []
            prod   = data['product'] if data.has_key('product') else []
            #logger.info(data)
        except:
            status = None
        if status:
            datas = domains.objects.filter(status__in=status, group__id__in=group, product__in=prod).all().order_by('-id')[:num]
        else:
            return HttpResponse(u"参数错误！")

        logger.info(u'查询参数：%s' %data)
        domain_list = []
        for domain in datas:
            tmp_dict = {}
            tmp_dict['id']      = domain.id
            tmp_dict['name']    = domain.name
            tmp_dict['product'] = domain.get_product_display()
            tmp_dict['group']   = domain.group.group
            tmp_dict['content'] = domain.content
            tmp_dict['status']  = domain.status

            domain_list.append(tmp_dict)
        return HttpResponse(json.dumps(domain_list))
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def GetGroups(request):
    if request.method == 'POST':
        return HttpResponse('You get nothing!')
    elif request.method == 'GET':
        clientip = getIp(request)
        logger.info('[GET]%s is requesting. %s' %(clientip, request.get_full_path()))

        datas = groups.objects.all()
        items = {}
        items['product_l'] = settings.choices_prod
        items['group_l']   = []
        for group in datas:
            tmp_dict = {}
            tmp_dict['id']     = group.id
            tmp_dict['group']  = group.group
            tmp_dict['client'] = group.client
            tmp_dict['method'] = group.method
            tmp_dict['ssl']    = group.ssl
            tmp_dict['retry']  = group.retry

            items['group_l'].append(tmp_dict)
        #logger.info(items)
        return HttpResponse(json.dumps(items))
    else:
        return HttpResponse('nothing!')

@csrf_exempt 
def DomainsUpdateStatus(request):
    if request.method == 'POST':
        clientip = getIp(request)
        data = json.loads(request.body)
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))
        if not HasPermission(request.user, 'change', 'detect', 'domains'):
            return HttpResponseForbidden('你没有修改的权限。')
        info = domains.objects.get(id=data['id'])
        info.status = data['status']
        info.save()
        return HttpResponse('更新成功！')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')
        
@csrf_exempt 
def DomainsDelete(request):
    if request.method == 'POST':
        clientip = getIp(request)
        datas = json.loads(request.body)
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), datas))
        if not HasPermission(request.user, 'delete', 'detect', 'domains'):
            return HttpResponseForbidden('你没有删除的权限。')
        for data in datas:
            info = domains.objects.get(id=data['id'])
            info.delete()
        return HttpResponse('删除成功！')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt 
def DomainsAdd(request):
    if request.method == 'POST':
        clientip = getIp(request)
        datas = json.loads(request.body)
        logger.info('%s is requesting. %s datas: %s' %(clientip, request.get_full_path(), datas))
        if not HasPermission(request.user, 'add', 'detect', 'domains'):
            return HttpResponseForbidden('你没有新增的权限。')
            
        group = groups.objects.get(id=datas['group'])
        exist = []
        for domain in datas['domain_l']:
            domain = domain.strip(' ')
            try:
                if domains.objects.get(name=domain): 
                    exist.append(domain)
                    continue
            except:
                info = domains(name=domain, product=datas['product'], group=group, content=datas['content'], status=datas['status'])
                info.save()
        if exist:
            return HttpResponse(str(exist)+'已存在，其余的新增成功！')
        else:
            return HttpResponse('新增成功！')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt 
def DomainsUpdate(request):
    if request.method == 'POST':
        clientip = getIp(request)
        datas = json.loads(request.body)
        logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
        if not HasPermission(request.user, 'change', 'detect', 'domains'):
            return HttpResponseForbidden('你没有修改的权限。')

        if len(datas['all']) == 1:
            group = groups.objects.get(id=datas['group'])
            info = domains.objects.get(id=datas['id'])
            info.name    = datas['name'][0]
            info.product = datas['product']
            info.group   = group
            info.content = datas['content']
            info.status  = datas['status']
            info.save()
        else:
            i = 0
            for line in datas['all']:
                if datas['group']:
                    group = groups.objects.get(id=int(datas['group']))
                else:
                    group = groups.objects.get(group=line['group'])
                info = domains.objects.get(id=line['id'])
                info.name    = datas['name'][i]
                info.product = datas['product'] if datas['product'] else prod_d[line['product']]
                info.group   = group
                info.content = datas['content'] if datas['content'] else line['content']
                info.status  = datas['status'] if datas['status'] else line['status']
                info.save()
                i += 1

        return HttpResponse('更新成功！')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')
        
@require_websocket
@csrf_exempt
def ProjectCheckServer(request):
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
        #logger.info(dir(request.websocket))
        #message = request.websocket.wait()
        code_list = ['200' ,'301' ,'302' ,'303' ,'405']
        rewrite_list = ['301' ,'302' ,'303']
        for postdata in request.websocket:
            #logger.info(type(postdata))
            data = json.loads(postdata)
            ### step one ###
            info_one = {}
            info_one['step'] = 'one'
            request.websocket.send(json.dumps(info_one))
            logger.info(u'%s is requesting. %s 执行参数：%s' %(clientip, request.get_full_path(), data))
            #results = []
            ### final step ###
            info_final = {}
            info_final['step'] = 'final'

            info_final['access_time'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            minion_list = minion_t.objects.filter(minion_id=data['minion_id'], status=1).all()

            info_final['code'] = "\n\t"

            for minion in minion_list:
                url = "http://" + minion.ip_addr + data['uri']

                try:
                    ret = requests.head(url, headers={'Host': data['domain']}, timeout=10)
                    info_final['code'] += u'%s - %s\n\t' %(ret.status_code, url)
                    if str(ret.status_code) in rewrite_list:
                        url = ret.headers['Location'].replace(data['domain'], minion.ip_addr)
                        try:
                            ret_r = requests.head(url, headers={'Host': data['domain']}, verify=False, timeout=10)
                            info_final['code'] += u'%s - %s\n\t' %(ret_r.status_code, url)
                        except:
                            info_final['code'] += u'%s - %s\n\t' %(error_status, url)
                except:
                    info_final['code'] += u'%s - %s\n\t' %(error_status, url)

            request.websocket.send(json.dumps(info_final))
        ### close websocket ###
        request.websocket.close()