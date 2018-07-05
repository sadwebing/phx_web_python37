# coding: utf8
from django.http     import HttpResponse
from accounts.limit  import LimitAccess
from phxweb          import settings
from accounts.views  import getIp
from tencent_api     import tcApi
from ws_api          import wsApi
from detect.models   import domains
from monitor.models  import cdn_proj_t
from accounts.models import cdn_t
from dwebsocket      import require_websocket, accept_websocket
from detect.telegram import sendTelegram
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json, logging, time, urlparse
logger = logging.getLogger('django')

#telegram 参数
message = settings.message_ONLINE

@csrf_exempt
def refleshGetProject(request):
    if request.method == 'POST':
        clientip = getIp(request)
        logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))

        projectlist = []
        cdn_prots   = cdn_proj_t.objects.all()
        for prot in cdn_prots:
            tmpdict = {}
            tmpdict['project'] = prot.get_project_display()
            tmpdict['domain']  = [ {'id': domain.id,
                                    'name': urlparse.urlsplit(domain.name).scheme+"://"+urlparse.urlsplit(domain.name).netloc,
                                    'product': domain.get_product_display()} for domain in prot.domain.all() if domain.cdn.all() ]
            #tmpdict['cdn']     = [ {'name': cdn.get_name_display(),
            #                        'account': cdn.account} for cdn in cdn_t.objects.all() ]
            projectlist.append(tmpdict)
        return HttpResponse(json.dumps(projectlist))

    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')


@csrf_exempt
def refleshPurge(request):
    if request.method == 'POST':
        clientip = getIp(request)
        cdn_d = {}
        info  = {'failed': [], 'sccess': []}
        data  = json.loads(request.body)
        cdns  = cdn_t.objects.all()
        for cdn in cdns:
            cdn_d[cdn.get_name_display()+"_"+cdn.account] = {
                'name': cdn.get_name_display(),
                'domain': [],
                'secretid': str(cdn.secretid),
                'secretkey': str(cdn.secretkey),
                'failed': [],
                'sccess': [],
            }
        
        cdn_proj_l = cdn_proj_t.objects.filter(project__in = data['cdn_proj']).all()
        for cdn_proj in cdn_proj_l:
            for domain in cdn_proj.domain.all():
                for cdn in domain.cdn.all():
                    cdn_d[cdn.get_name_display()+"_"+cdn.account]['domain'].append(urlparse.urlsplit(domain.name).scheme+"://"+urlparse.urlsplit(domain.name).netloc)
        for cdn in cdn_d:
            info['cdn'] = cdn
            if cdn_d[cdn]['domain']:
                #开始清缓存，判断CDN接口是否存在
                if cdn_d[cdn]['name'] == "tencent":
                    req = tcApi(cdn_d[cdn]['secretid'], cdn_d[cdn]['secretkey'])
                elif cdn_d[cdn]['name'] == "wangsu":
                    req = wsApi(cdn_d[cdn]['secretid'], cdn_d[cdn]['secretkey'])
                else:
                    cdn_d[cdn]['failed'].append("%s: 接口不存在！" %cdn)
                    continue

                while len(cdn_d[cdn]['domain']) != 0 :
                    domains_c            = cdn_d[cdn]['domain'][:10]
                    cdn_d[cdn]['domain'] = cdn_d[cdn]['domain'][10:]

                    for uri in data['uri']:
                        result, status = req.purge(domains_c, uri)
                        if status:
                            cdn_d[cdn]['sccess'] += [ domain+uri for domain in domains_c ]
                        else:
                            cdn_d[cdn]['failed'] += [ domain+uri for domain in domains_c ]
        for cdn in cdn_d:
            if cdn_d[cdn]['failed']:
                message["text"] = cdn_d[cdn]['failed']
                message['caption'] = cdn + ': 域名缓存清理失败!'
                sendTelegramRe(message)
            if cdn_d[cdn]['sccess']:
                message["text"] = cdn_d[cdn]['sccess']
                message['caption'] = cdn + ': 域名缓存清理成功。'
                sendTelegramRe(message)

        return HttpResponse('success!')
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

def sendTelegramRe(message):
    if len(message["text"]) > 10:
        message["text"] = '\n'.join(message["text"])
        message["doc"] = True
        message['doc_name'] = 'domain.txt'
    else:
        message["doc"] = False
        message["text"] = '\r\n'.join(message["text"]) +'\r\n'+ message['caption']
    sendTelegram(message).send()

@accept_websocket
@csrf_exempt
def refleshExecute(request):
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    clientip = getIp(request)
    
    if request.is_websocket():
        for postdata in request.websocket:
            data = json.loads(postdata)
            logger.info('%s is requesting. %s 执行参数：%s' %(clientip, request.get_full_path(), data))
            ### step one ##
            info = {}
            info['step'] = 'one'
            request.websocket.send(json.dumps(info))
            #time.sleep(2)
            ### two step ###
            info['step'] = 'two'
            cdn_d = {}
            cdns  = cdn_t.objects.all()
            for cdn in cdns:
                cdn_d[cdn.get_name_display()+"_"+cdn.account] = {
                    'name': cdn.get_name_display(),
                    'domain': [],
                    'secretid': str(cdn.secretid),
                    'secretkey': str(cdn.secretkey),
                    'failed': [],
                    'sccess': [],
                }

            domain_l = domains.objects.filter(id__in=data['domain']).all()
            logger.info(domain_l)
            for domain in domain_l:
                for cdn in domain.cdn.all():
                    cdn_d[cdn.get_name_display()+"_"+cdn.account]['domain'].append(urlparse.urlsplit(domain.name).scheme+"://"+urlparse.urlsplit(domain.name).netloc)
            #logger.info(cdn_d)
            for cdn in cdn_d:
                info['cdn'] = cdn
                if cdn_d[cdn]['domain']:
                    #开始清缓存，判断CDN接口是否存在
                    if cdn_d[cdn]['name'] == "tencent":
                        req = tcApi(cdn_d[cdn]['secretid'], cdn_d[cdn]['secretkey'])
                    elif cdn_d[cdn]['name'] == "wangsu":
                        req = wsApi(cdn_d[cdn]['secretid'], cdn_d[cdn]['secretkey'])
                    else:
                        info['result'] = ["CDN 接口不存在！"]
                        cdn_d[cdn]['failed'].append("%s: 接口不存在！" %cdn)
                        request.websocket.send(json.dumps(info))
                        continue

                    while len(cdn_d[cdn]['domain']) != 0 :
                        domains_c            = cdn_d[cdn]['domain'][:10]
                        cdn_d[cdn]['domain'] = cdn_d[cdn]['domain'][10:]

                        for uri in data['uri']:
                            result, status = req.purge(domains_c, uri)
                            if status:
                                info['result'] = [ domain+uri+": 清缓存成功。" for domain in domains_c ]
                                cdn_d[cdn]['sccess'] += [ domain+uri for domain in domains_c ]
                            else:
                                info['result'] = [ domain+uri+": 清缓存失败！" for domain in domains_c ]
                                cdn_d[cdn]['failed'] += [ domain+uri for domain in domains_c ]
                            request.websocket.send(json.dumps(info))
            info['step'] = 'final'
            request.websocket.send(json.dumps(info))
            for cdn in cdn_d:
                if cdn_d[cdn]['failed']:
                    message["text"] = cdn_d[cdn]['failed']
                    message['caption'] = cdn + ': 域名缓存清理失败!'
                    sendTelegramRe(message)
                if cdn_d[cdn]['sccess']:
                    message["text"] = cdn_d[cdn]['sccess']
                    message['caption'] = cdn + ': 域名缓存清理成功。'
                    sendTelegramRe(message)
            request.websocket.close()
            break
        ### close websocket ###
        request.websocket.close()
    else:
        return HttpResponse('nothing!', status=500)