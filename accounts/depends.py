# coding: utf-8
from django.shortcuts               import render
from django.http                    import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.template.response       import TemplateResponse
from django.utils.http              import is_safe_url, urlsafe_base64_decode
from accounts.limit                 import LimitAccess
from dns.models                     import alter_history

import logging, datetime
logger = logging.getLogger('django')

def insert_ah(clientip, username, pre_rec, now_rec, result=True, action='change'):
    logger.info("req_ip: %s | user: %s | %s-record: { %s } ---> { %s } {result: %s}" %(clientip, username, action, pre_rec, now_rec, result))

    insert_h = alter_history(
            time    = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            req_ip  = clientip,
            user    = username,
            pre_rec = pre_rec,
            now_rec = now_rec,
            action  = action,
            status  = result,
        )

    insert_h.save()