#coding: utf-8
from django.conf.urls import url, include
from . import views

urlpatterns = [
    #saltstack 调用
    url('^check_minion$', views.CheckMinion),
    url('^command$', views.command),
    url('^deploy$', views.deploy),
    url('^restart/get_project$', views.GetProjectActive),
    url('^restart/get_project_servers$', views.GetProjectServers),
    url('^command/execute$', views.CommandExecute),
    url('^command/deploy$', views.CommandDeploy),
    url('^deploy/deploy$', views.DeployExe),
    url('^saltstack_id$', views.Id),
    url('^saltstack_id/Query$', views.IdQuery),
    url('^saltstack_id/QueryMinion$', views.QueryMinion),
    url('^$', views.command),

    #缓存清理
    url('^reflesh$', views.reflesh),
    url('^reflesh/get_domains$', views.refleshGetDomains),
    url('^reflesh/get_project$', views.refleshGetProject),
    url('^reflesh/execute$', views.refleshExecute),
    url('^reflesh/execute_cdn$', views.refleshExecuteCdn),
    url('^reflesh/purge$', views.refleshPurge),
    
]
