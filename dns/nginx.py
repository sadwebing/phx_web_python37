# coding: utf8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from dwebsocket import require_websocket
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from dns.cf_api import CfApi
from dns.cf import *
from dns.models import cf_account
import json, logging, requests, re, datetime
logger = logging.getLogger('django')


@csrf_protect
@login_required
def Nginx(request):
    title = u'CloudFlare-主页'
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

    product_list = cf_account.objects.values_list("name").all().order_by("name")
    logger.info('%s %s' %(type(product_list), product_list))

    return render(
        request,
        'dns/nginx.html',
        {
            'title': title,
            'clientip':clientip,
            'role': role,
            'username': username,
            'product_list': [name[0] for name in product_list],
        }
    )
