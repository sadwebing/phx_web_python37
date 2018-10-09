# coding: utf8
from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponse, HttpResponseForbidden
from dwebsocket                     import require_websocket
from django.views.decorators.csrf   import csrf_exempt, csrf_protect
from monitor.models                 import project_t, minion_t
from detect.models                  import domains, groups, cdn_account_t
from dns.models                     import cf_account
from saltstack.command              import Command
from accounts.views                 import HasPermission, getIp
from phxweb                         import settings
import json, logging, requests, re, datetime

logger = logging.getLogger('django')
error_status = 'null'

prod_d = {}
for line in settings.choices_product:
    prod_d[line[1]] = line[0]
cust_d = {}
for line in settings.choices_customer:
    cust_d[line[1]] = line[0]

def takeId(elem):
    return elem['id']

@csrf_exempt
def DomainsQuery(request):
    if request.method == 'GET':
        return HttpResponse('You get nothing!')
    elif request.method == 'POST':
        clientip = getIp(request)
        logger.info('[POST]%s is requesting. %s' %(clientip, request.get_full_path()))
        try:
            data     = json.loads(request.body)
            status   = list(data['status']) if data.has_key('status') else None
            num      = int(data['num']) if data.has_key('num') and str(data['num']).lower() != 'all' else None
            group    = data['group'] if data.has_key('group') else []
            product  = data['product'] if data.has_key('product') else []
            customer = data['customer'] if data.has_key('customer') else []
            cdn      = data['cdn'] if data.has_key('cdn') else []
            cf       = data['cf'] if data.has_key('cf') else []
            #logger.info(data)
        except:
            status = None
        if status:
            domains_ft = domains.objects.filter(status__in=status, group__id__in=group, product__in=product, customer__in=customer)
            if len(cdn) != 0:
                domains_ft = domains_ft.filter(cdn__in=cdn)
            if len(cf) != 0:
                domains_ft = domains_ft.filter(cf__in=cf)
            datas = domains_ft.all().order_by('-id')[:num]

            #if len(cdn) == 0:
            #    datas = domains.objects.filter(status__in=status, group__id__in=group, product__in=product, customer__in=customer).all().order_by('-id')[:num]
            #else:
            #    datas = domains.objects.filter(status__in=status, group__id__in=group, product__in=product, customer__in=customer, cdn__in=cdn, cf__in=cf).all().order_by('-id')[:num]
        else:
            return HttpResponseServerError(u"参数错误！")

        logger.info(u'查询参数：%s' %data)
        domain_list = []
        for domain in list(set(datas)):
            tmp_dict = {}
            tmp_dict['id']       = domain.id
            tmp_dict['name']     = domain.name
            tmp_dict['product']  = domain.get_product_display()
            tmp_dict['customer'] = domain.get_customer_display()
            tmp_dict['group']    = domain.group.group
            tmp_dict['content']  = domain.content
            tmp_dict['status']   = domain.status
            tmp_dict['cdn']      = [{
                    'id':      cdn.id,
                    'name':    cdn.get_name_display(),
                    'account': cdn.account,
                } for cdn in domain.cdn.all()]
            tmp_dict['cf']       = [{
                    'id':      cf.id,
                    'name':    "cloudflare",
                    'account': cf.name,
                } for cf in domain.cf.all()]

            domain_list.append(tmp_dict)
        #logger.info(domain_list)
        domain_list.sort(key=takeId, reverse=True) #以ID 倒序排序
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

        cdns   = cdn_account_t.objects.all()
        group  = groups.objects.all()
        items  = {
                'customer_l': settings.choices_customer,
                'product_l' : settings.choices_product,
                'group_l'   : [],
                'cdn_l'     : [],
                'cf_l'      : [],
            }

        cf_ac  = cf_account.objects.all()

        for cdn in cdns:
            tmp_dict = {
                'id':      cdn.id,
                'name':    cdn.get_name_display(),
                'account': cdn.account,
            }

            items['cdn_l'].append(tmp_dict)

        for cf in cf_ac:
            tmp_dict = {
                'id':      cf.id,
                'name':    "cloudflare",
                'account': cf.name,
            }
            items['cf_l'].append(tmp_dict)

        for item in group:
            tmp_dict = {}
            tmp_dict['id']     = item.id
            tmp_dict['group']  = item.group
            tmp_dict['client'] = item.client
            tmp_dict['method'] = item.method
            tmp_dict['ssl']    = item.ssl
            tmp_dict['retry']  = item.retry

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
        if not HasPermission(request.user, 'change', 'domains', 'detect'):
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
        if not HasPermission(request.user, 'delete', 'domains', 'detect'):
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
        if not HasPermission(request.user, 'add', 'domains', 'detect'):
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
                info = domains(
                        name=domain, 
                        product=datas['product'], 
                        customer=datas['customer'], 
                        group=group, 
                        content=datas['content'], 
                        #cdn=[cdn_account_t.objects.get(id=id) for id in datas['cdn']], 
                        status=datas['status']
                    )
                logger.info(datas)
                info.save()
                for id in datas['cdn']:
                    info.cdn.add(cdn_account_t.objects.get(id=id))
                    info.save()
                for id in datas['cf']:
                    info.cf.add(cf_account.objects.get(id=id))
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
        if not HasPermission(request.user, 'change', 'domains', 'detect'):
            return HttpResponseForbidden('你没有修改的权限。')

        i = 0
        for line in datas['all']:
            if datas['group']:
                group = groups.objects.get(id=int(datas['group']))
            else:
                group = groups.objects.get(group=line['group'])

            info = domains.objects.get(id=line['id'])
            if int(datas['edit_cdn_bool'][0]) == 1:
                for cdn in info.cdn.all():
                    info.cdn.remove(cdn)
                    info.save()
                    #info.cdn.all().delete()
                for id in datas['cdn']:
                    info.cdn.add(cdn_account_t.objects.get(id=id))
                    info.save()
            if int(datas['edit_cf_bool'][0]) == 1:
                for cf in info.cf.all():
                    info.cf.remove(cf)
                    info.save()
                    #info.cf.all().delete()
                for id in datas['cf']:
                    info.cf.add(cf_account.objects.get(id=id))
                    info.save()
            info.name     = datas['domain_l'][i]
            info.product  = datas['product'] if datas['product'] else prod_d[line['product']]
            info.customer = datas['customer'] if datas['customer'] else cust_d[line['customer']]
            info.group    = group
            info.content  = datas['content'] if datas['content'] else line['content']
            info.status   = datas['status'] if datas['status'] else line['status']
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