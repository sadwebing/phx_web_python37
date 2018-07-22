# coding: utf-8
from django.shortcuts               import render
from django.http                    import HttpResponse
from django.views.decorators.csrf   import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from phxweb                         import settings
from saltstack.saltapi              import SaltAPI
from dwebsocket                     import require_websocket, accept_websocket
from monitor.models                 import project_t, minion_t, minion_ip_t
from command                        import Command
from accounts.limit import LimitAccess
from accounts.views import getIp
from reflesh        import *
import json, logging, time
logger = logging.getLogger('django')


# Create your views here.
@csrf_exempt
def GetProjectActive(request):
    if request.method == 'POST':
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            clientip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            clientip = request.META['REMOTE_ADDR']

        datas     = project_t.objects.filter(status=1)
        projectlist = []
        for data in datas:
            tmpdict = {}
            tmpdict['envir']       = data.get_envir_display()
            tmpdict['product']     = data.get_product_display()
            tmpdict['project']     = data.get_project_display()
            tmpdict['server_type'] = data.get_server_type_display()
            tmpdict['minion_id']   = [minion.minion_id for minion in data.minion_id.filter(status=1).all()]
            projectlist.append(tmpdict)
        logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
        #logger.info(projectlist)
        return HttpResponse(json.dumps(projectlist))
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def GetProjectServers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #logger.info(data.getlist('project'))
        logger.info(request.body)
        clientip = request.META['REMOTE_ADDR']
        server_dict = {}
        for project in data['project']:
            datas     = project_t.objects.filter(project=project)
            serverlist = []
            for data in datas:
                tmpdict = {}
                tmpdict['minion_id'] = data.minion_id
                tmpdict['ip_addr'] = data.ip_addr
                tmpdict['role'] = data.role
                tmpdict['status'] = data.status
                tmpdict['info'] = data.info
                tmpdict['envir'] = data.envir
                serverlist.append(tmpdict)
            server_dict[project] = serverlist
        logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
        return HttpResponse(json.dumps(server_dict))
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')
  
@accept_websocket     
@csrf_exempt
def CheckMinion(request):
    global username, role, clientip
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    clientip = request.META['REMOTE_ADDR']
    if request.is_websocket():
        for postdata in request.websocket:
            data = json.loads(postdata)
            logger.info('%s is requesting. %s 执行参数：%s' %(clientip, request.get_full_path(), data))
            result = {}
            for minion_id in data:
                commandexe = Command(minion_id, 'test.ping')
                result['minion_id'] = minion_id
                result['test_ping'] = commandexe.TestPing()[minion_id]
                request.websocket.send(json.dumps(result))
        ### close websocket ###
        request.websocket.close()
    else:
        if request.method == 'POST':
            #print request.body
            #return HttpResponse("%s" %request.body)
            data = json.loads(request.body)
            result = {}
            for tgt in data['tgt']:
                logger.info('%s is requesting %s. data: %s' %(clientip, request.get_full_path(), data))
                #logger.info('%s' %(data['tgt']))
                commandexe = Command(tgt, 'test.ping')
                result[tgt] = commandexe.TestPing()[tgt]
                logger.info(result)
            return HttpResponse(json.dumps(result))
        elif request.method == 'GET':
            logger.info('%s is requesting %s.' %(clientip, request.get_full_path()))
            return HttpResponse('You get nothing!')
        else:
            logger.info('%s is requesting %s.' %(clientip, request.get_full_path()))
            return HttpResponse('nothing!')

@require_websocket
@csrf_exempt
def CommandExecute(request):
    if request.is_websocket():
        global username, role, clientip
        username = request.user.username
        try:
            role = request.user.userprofile.role
        except:
            role = 'none'
        clientip = request.META['REMOTE_ADDR']
        for postdata in request.websocket:
            if not postdata:
                break
            data = json.loads(postdata)
            logger.info('%s is requesting. %s 执行参数：%s' %(clientip, request.get_full_path(), data))
            #request.websocket.send(json.dumps(data))
            ### step one ##
            info_one = {}
            info_one['step'] = 'one'
            request.websocket.send(json.dumps(info_one))
            #time.sleep(2)
            ### final step ###
            info_final = {}
            info_final['step'] = 'final'
            arglist = ["runas=%s" %data['exe_user']]
            arglist.append(data['arguments'])
            commandexe = Command(data['target'], data['function'], arglist, data['expr_form'],)
            if data['function'] == 'test.ping':
                info_final['results'] = commandexe.TestPing()
            elif data['function'] == 'cmd.run':
                info_final['results'] = commandexe.CmdRun()
            elif data['function'] == 'state.sls':
                info_final['results'] = commandexe.StateSls(data['arguments'])
            #logger.info(json.dumps(info_final))

            request.websocket.send(json.dumps(info_final))
        ### close websocket ###
        request.websocket.close()

@require_websocket
@csrf_exempt
def CommandDeploy(request):
    if request.is_websocket():
        global username, role, clientip
        username = request.user.username
        try:
            role = request.user.userprofile.role
        except:
            role = 'none'
        clientip = request.META['REMOTE_ADDR']
        #logger.info(dir(request.websocket))
        #message = request.websocket.wait()
        for postdata in request.websocket:
            if not postdata:
                break
            #logger.info(type(postdata))
            data = json.loads(postdata)
            ### step one ###
            info_one = {}
            info_one['step'] = 'one'
            info_one['project'] = data['project']
            info_one['minion_id'] = data['minion_id']
            request.websocket.send(json.dumps(info_one))
            logger.info('%s is requesting. %s 执行参数：%s' %(clientip, request.get_full_path(), data))

            ### final step ###
            info_final = {}
            info_final['step'] = 'final'

            commandexe = Command(data['minion_id'], 'state.sls', expr_form='list')
            info_final['results'] = commandexe.StateSls('nginx.conf')
            info_final['results'] = commandexe.StateSls('nginx.reload')
            #info_final['results'] = dict(info_final['results'], **commandexe.StateSls('nginx.reload'))

            request.websocket.send(json.dumps(info_final))
        ### close websocket ###
        request.websocket.close()

@accept_websocket     
@csrf_exempt
def DeployExe(request):
    global username, role, clientip
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    clientip = request.META['REMOTE_ADDR']
    if request.is_websocket():
        for postdata in request.websocket:
            logger.info('%s is requesting. %s 执行参数：%s' %(clientip, request.get_full_path(), postdata))
            #logger.info(type(postdata))
            data = json.loads(postdata)
            ### step one ###
            info_one = {}
            info_one['step'] = 'one'
            request.websocket.send(json.dumps(info_one))   
            time.sleep(1)
            ### final step ###
            info_final = {}
            info_final['step'] = 'final'
            info_final['minion_all'] = len(data['minion_id'])
            info_final['minion_count'] = 0

            #set timeout for specific module
            if data['module'] == 'init':
                timeout = 600
            elif data['module'] == 'tomcat':
                timeout = 1200
            elif data['module'] == 'php':
                timeout = 1800
            else:
                timeout = 300

            #execute deploy module
            for minion_id in data['minion_id']:
                info_final['minion_id'] = minion_id
                info_final['module'] = data['module']
                info_final['project'] = data['project']
                info_final['result'] = ""
                request.websocket.send(json.dumps(info_final))
                logger.info('部署参数：%s' %info_final)
                info_final['minion_count'] += 1
                if data['module'] == 'tomcat':
                    commandexe = Command('WTT_100_109', 'cmd.run', '/srv/shell/install_tomcat.sh %s %s' %(minion_id, data['project']), 'glob', timeout=timeout)
                    info_final['result'] = commandexe.CmdRun()['WTT_100_109']
                    logger.info("%s 部署完成。" %data['project'])
                else:
                    commandexe = Command(minion_id, 'state.sls', data['module'], 'glob', timeout=timeout)
                    info_final['result'] = commandexe.StateSls()[minion_id]
                    logger.info("%s 部署完成。" %data['module'])
                request.websocket.send(json.dumps(info_final))
        ### close websocket ###
        #request.websocket.close()

@csrf_protect
@login_required
def command(request):
    global username, role, clientip
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    try:
        manage = request.user.userprofile.manage
    except:
        manage = 0
    clientip = request.META['REMOTE_ADDR']
    title = u'SALTSTACK-命令管理'
    logger.info('%s is requesting.' %clientip)
    return render(
        request,
        LimitAccess(role, 'saltstack/saltstack_index.html'),
        {
            'clientip':clientip,
            'title': title,
            'role': role,
            'manage': manage,
            'username': username,
        }
    )

@csrf_protect
@login_required
def deploy(request):
    global username, role, clientip
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    global clientip
    clientip = request.META['REMOTE_ADDR']
    title = u'SALTSTACK-模块部署'
    logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
    return render(
        request,
        LimitAccess(role, 'saltstack/saltstack_deploy.html'),
        {
            'clientip':clientip,
            'title': title,
            'role': role,
            'username': username,
        }
    )

@csrf_protect
@login_required
def Id(request):
    global username, role, clientip
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    global clientip
    clientip = request.META['REMOTE_ADDR']
    title = u'SALTSTACK-ID管理'
    logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
    return render(
        request,
        LimitAccess(role, 'saltstack/saltstack_id.html'),
        {
            'clientip':clientip,
            'title': title,
            'role': role,
            'username': username,
        }
    )

@csrf_exempt
def IdQuery(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        sapi = SaltAPI(
            url      = settings.SALT_API['url'],
            username = settings.SALT_API['user'],
            password = settings.SALT_API['password']
            )
        minionsup, minionsdown= sapi.MinionStatus()
        minion_list = []
        logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
        for minion_id in minionsup:
            minion_dict = {}
            minion_dict['minion_id'] = minion_id
            minion_dict['minion_status'] = 'up'
            minion_list.append(minion_dict)
        for minion_id in minionsdown:
            minion_dict = {}
            minion_dict['minion_id'] = minion_id
            minion_dict['minion_status'] = 'down'
            minion_list.append(minion_dict)
        return HttpResponse(json.dumps(minion_list))
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_exempt
def QueryMinion(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        sapi = SaltAPI(
            url      = settings.SALT_API['url'],
            username = settings.SALT_API['user'],
            password = settings.SALT_API['password']
            )
        data = json.loads(request.body)
        logger.info('%s is requesting %s. minion: %s' %(clientip, request.get_full_path(), data))
        minion_id = data[0]['minion_id']
        info = sapi.GetGrains(minion_id)
        #logger.info(info['return'][0])
        return HttpResponse(json.dumps(info['return'][0]))
    elif request.method == 'GET':
        return HttpResponse('You get nothing!')
    else:
        return HttpResponse('nothing!')

@csrf_protect
@login_required
def reflesh(request):
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    try:
        manage = request.user.userprofile.manage
    except:
        manage = 0

    clientip = getIp(request)
    title = u'缓存清理'
    logger.info('%s is requesting. %s' %(clientip, request.get_full_path()))
    return render(
        request,
        'saltstack/reflesh.html',
        {
            'clientip':clientip,
            'title': title,
            'role': role,
            'username': username,
            'manage': manage,
        }
    )
