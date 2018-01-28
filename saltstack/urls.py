from django.conf.urls import url, include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url('^check_minion$', views.CheckMinion),
    url('^command$', views.command),
    url('^deploy$', views.deploy),
    url('^restart/get_project$', views.GetProjectActive),
    url('^restart/get_project_servers$', views.GetProjectServers),
    url('^command/execute$', views.CommandExecute),
    url('^command/restart$', views.CommandRestart),
    url('^deploy/deploy$', views.DeployExe),
    url('^saltstack_id$', views.Id),
    url('^saltstack_id/Query$', views.IdQuery),
    url('^saltstack_id/QueryMinion$', views.QueryMinion),
    url('^$', views.command),
]
