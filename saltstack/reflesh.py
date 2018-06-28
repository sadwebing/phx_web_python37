# coding: utf8
from django.http     import HttpResponse
from accounts.limit  import LimitAccess
from phxweb          import settings
from accounts.views  import getIp
from tencent_api     import tcApi
from ws_api          import wsApi
from monitor.models  import cdn_proj_t, cdn_t
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
            tmpdict['domain']  = [ {'name': urlparse.urlsplit(domain.name).scheme+"://"+urlparse.urlsplit(domain.name).netloc,
                                    'product': domain.get_product_display()} for domain in prot.domain.all() ]
            tmpdict['cdn']     = [ {'name': cdn.get_name_display(),
                                    'account': cdn.account} for cdn in prot.cdn.all() ]
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
        data     = json.loads(request.body)
        secretid = 'AKID75tX0ViCMVbcVJoqmbFjCfx35wNsshIs'
        secretkey = 'c5QehaK1bQ9oKoDpOsNsiPvHSbdYQKB1'
        req = tcApi(secretid, secretkey)
        result, status = req.purge(data['domains'], data['uri'])
        
        if status:
            return HttpResponse(json.dumps(result))
        else:
            return HttpResponse(json.dumps(result))
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

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
                cdn_d[cdn.get_name_display()+"_"+cdn.account] = cdn
            for cdn in data['cdn']:
                info['cdn'] = cdn
                secretid  = cdn_d[cdn].secretid
                secretkey = cdn_d[cdn].secretkey
                if cdn.split('_')[0] == "tencent":
                    req = tcApi(secretid, secretkey)
                elif cdn.split('_')[0] == "wangsu":
                    req = wsApi(secretid, secretkey)
                else:
                    info['result'] = ["CDN 接口不存在！"]
                    message["text"] += "%s: CDN 接口不存在！\r\n" %cdn
                    request.websocket.send(json.dumps(info))
                    continue
                for uri in data['uri']:
                    result, status = req.purge(data['domain'], uri)
                    if status:
                        info['result'] = [ domain+uri+": 刷新成功！" for domain in data['domain'] ]
                        message["text"] += cdn + ": \r\n" + "\r\n".join(info['result']) 
                    else:
                        info['result'] = [ domain+uri+": 刷新失败！" for domain in data['domain'] ]
                        message["text"] += cdn + ": \r\n" + "\r\n".join(info['result']) 
                    request.websocket.send(json.dumps(info))
            info['step'] = 'final'
            request.websocket.send(json.dumps(info))
            sendTelegram(message).send()
        ### close websocket ###
        request.websocket.close()
    else:
        return HttpResponse('nothing!', status=500)