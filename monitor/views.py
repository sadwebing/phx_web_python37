# coding: utf8
from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponse
from django.views.decorators.csrf   import csrf_exempt, csrf_protect
from accounts.limit                 import LimitAccess
from project                        import *
from domains                        import *
import json, logging
logger = logging.getLogger('django')


@csrf_protect
@login_required
def index(request):
    title = u'管理中心-主页'
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
    logger.info('%s is requesting %s' %(clientip, request.get_full_path()))
    return render(
        request,
        'index.html',
        {
            #'title': title,
            'clientip':clientip,
            'role': role,
            'username': username,
        }
    )

@csrf_protect
@login_required
def Services(request):
    title = u'monitor-监控列表'
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
    logger.info('%s is requesting %s' %(clientip, request.get_full_path()))
    return render(
        request,
        LimitAccess(role, 'monitor/monitor_index.html'),
        {
            'title': title,
            'clientip':clientip,
            'role': role,
            'username': username,
        }
    )
    
@csrf_protect
@login_required
def Domains(request):
    title = u'monitor-监控列表'
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
    logger.info('%s is requesting %s' %(clientip, request.get_full_path()))
    return render(
        request,
        LimitAccess(role, 'monitor/domains.html'),
        {
            'title': title,
            'clientip':clientip,
            'role': role,
            'username': username,
        }
    )
