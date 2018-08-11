# coding: utf-8
from django.shortcuts               import render
from django.http                    import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms      import AuthenticationForm
from django.views.decorators.debug  import sensitive_post_parameters
from django.views.decorators.csrf   import csrf_protect
from django.views.decorators.cache  import never_cache
from django.contrib.sites.shortcuts import get_current_site
from django.template.response       import TemplateResponse
from django.utils.http              import is_safe_url, urlsafe_base64_decode
from accounts.limit                 import LimitAccess
from django.contrib.auth.models     import User
from dns.models     import alter_history
from monitor.models import project_t
from models         import user_project_authority_t
from monitor.models import permission_t
from django.contrib.auth import (
                                REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
                                logout as auth_logout, update_session_auth_hash,
                            )
import logging, datetime
logger = logging.getLogger('django')

# Create your views here.

@csrf_protect
@login_required
def home(request):
    title = u'默认主页'
    global username, role, clientip
    username = request.user.username
    try:
        role = request.user.userprofile.role
    except:
        role = 'none'
    permissions = request.user.get_all_permissions()
    logger.info(permissions)
    if permissions:
        auth = 'welcome!'
    else:
        auth = 'you don\'t have any permissions.'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        clientip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        clientip = request.META['REMOTE_ADDR']
    logger.info('%s is requesting %s' %(clientip, request.get_full_path()))

    return render(
        request,
        'home/home.html',
        {
            'title': title,
            'clientip':clientip,
            'role': role,
            'username': username,
            'auth': auth,
            'permissions': permissions,
        }
    )

def logout(request):
    redirect_to = request.REQUEST.get('url', '/')
    auth_logout(request)
    
    return HttpResponseRedirect(redirect_to)

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
                redirect_field_name=REDIRECT_FIELD_NAME,
                authentication_form=AuthenticationForm,
                current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                            request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)

def HasDnsPermission(request, dns, account, permisson):
    if request.user.is_superuser:
        return True
    if dns == "dnspod" and request.user.userprofile.dns.filter(permission=permisson, dnspod_account__name=account):
        return True
    elif dns == "cf" and request.user.userprofile.dns.filter(permission=permisson, cf_account__name=account):
        return True
    else:
        return False

def HasPermission(user, act, table, app):
    #logger.error('%s don\'t have the permisson to %s table %s of %s' %(user.username, act, table, app))
    if not user.has_perm(app+'.'+act+'_'+table):
        logger.error('%s don\'t have the permisson to %s table %s of %s' %(user.username, act, table, app))
        return False
    else:
        return True
        
def getIp(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        clientip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        clientip = request.META['REMOTE_ADDR']
    return clientip

def getProjects(request, value):
    projects = []
    user = User.objects.get(username=request.user.username) #获取用户信息
    permission = permission_t.objects.get(permission=value) #权限
    if request.user.is_superuser:
        projects = project_t.objects.filter(status=1).all()
    else:
        try:
            authoritys = user_project_authority_t.objects.filter(user=user, permission__in=[permission]).all()
            for authority in authoritys:
                projects += [ project for project in authority.project.filter(status=1).all().order_by('product')]
        except:
            projects = []
    return projects

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