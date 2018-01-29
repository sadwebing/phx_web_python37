# coding: utf8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from dwebsocket import require_websocket
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from models import project_t, minion_t
from saltstack.command import Command
from accounts.views import HasPermission
import json, logging, requests, re, datetime
logger = logging.getLogger('django')
error_status = 'null'

@csrf_exempt
def ProjectQuery(request):
	if request.method == 'GET':
		return HttpResponse('You get nothing!')
	elif request.method == 'POST':
		clientip = request.META['REMOTE_ADDR']
		logger.info('[POST]%s is requesting. %s' %(clientip, request.get_full_path()))
		try:
			data = json.loads(request.body)
			act = data['act']
			#logger.info(data)
		except:
			act = 'null'
		if act == 'query_all':
			datas = project_t.objects.all()
		elif act == 'query_active':
			datas = project_t.objects.filter(status=1)
		elif act == 'query_inactive':
			datas = project_t.objects.filter(status=0)
		else:
			return HttpResponse(u"参数错误！")
		logger.info(u'查询参数：%s' %act)
		project_list = []
		for project in datas:
			if project.status == 1:
				state = 'active'
			elif project.status == 0:
				state = 'inactive'
			else:
				state = 'unknown'
			tmp_dict = {}
			tmp_dict['id'] = project.id
			tmp_dict['envir'] = project.envir
			tmp_dict['product'] = project.product
			tmp_dict['project'] = project.project
			tmp_dict['minion_id'] = project.minion_id
			tmp_dict['server_type'] = project.server_type
			tmp_dict['role'] = project.role
			tmp_dict['domain'] = project.domain
			tmp_dict['uri'] = project.uri
			tmp_dict['status_'] = state
			tmp_dict['info'] = project.info
			project_list.append(tmp_dict)
		return HttpResponse(json.dumps(project_list))
	else:
		return HttpResponse('nothing!')

@csrf_exempt 
def ProjectUpdateStatus(request):
    if request.method == 'POST':
        clientip = request.META['REMOTE_ADDR']
        data = json.loads(request.body)
        logger.info('%s is requesting. %s data: %s' %(clientip, request.get_full_path(), data))
        if not HasPermission(request.user, 'change', 'monitor', 'project_t'):
            return HttpResponseForbidden('你没有修改的权限。')
        info = project_t.objects.get(id=data['id'])
        info.status = data['status']
        info.save()
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