# coding: utf8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json, logging, requests, re, datetime
#import dnsn.resolver

logger = logging.getLogger('django')

@csrf_exempt 
def GetDns(request):
    if request.method == 'GET':
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            clientip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            clientip = request.META['REMOTE_ADDR']

        domain = request.GET.get('domain')

        logger.info('%s is requesting. %s domain: %s' %(clientip, request.get_full_path(), domain))

        #cname = dnsn.resolver.query(domain, 'CNAME').response.answer[0].items[0].__str__()

        return HttpResponse('cname')

    else:
        return HttpResponse('nothing!', status=500)