#-_- coding: utf-8 -_-
from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.http                    import HttpResponse
from django.views.decorators.csrf   import csrf_exempt, csrf_protect
from dwebsocket                     import require_websocket, accept_websocket
from models                         import domains
from accounts.limit                 import LimitAccess
import json, logging, requests, re

logger = logging.getLogger('django')

@csrf_exempt
def GetDomains(request):
    title = u'获取检测域名'
    clientip = request.META['REMOTE_ADDR']
    logger.info('%s is requesting %s' %(clientip, request.get_full_path()))
    domain_list = []

    if request.method == 'POST':
        try:
            product  = json.loads(request.body)['product']
            if product == 'all':
                domain_l = domains.objects.filter(status=1).all()
            else:
                domain_l = domains.objects.filter(status=1, product=json.loads(request.body)['product']).all()
        except Exception, e:
            logger.error(e.message)
            domain_l = []

        for domain in domain_l:
            tmp_dict = {}
            tmp_dict['name']   = domain.name
            tmp_dict['client'] = domain.group.client
            tmp_dict['method'] = domain.group.method
            tmp_dict['ssl']    = domain.group.ssl
            domain_list.append(tmp_dict)
        return HttpResponse(json.dumps(domain_list))