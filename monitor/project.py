# coding: utf8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from dwebsocket import require_websocket
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from models import project_t, minion_t
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
			datas = project_t.objects.filter(status='active')
		elif act == 'query_inactive':
			datas = project_t.objects.filter(status='inactive')
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

