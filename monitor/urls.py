# coding: utf8
from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url('^services$', views.Services, name='Services'),
    url('^project/Query$', views.ProjectQuery, name='ProjectQuery'),
    url('^project/UpdateStatus$', views.ProjectUpdateStatus, name='ProjectUpdateStatus'),
    url('^project/CheckServer$', views.ProjectCheckServer, name='ProjectCheckServer'),
    
    #域名监控
    url('^domains$', views.Domains, name='Domains'),
    url('^domains/getGroups$', views.GetGroups, name='GetGroups'),
    url('^domains/Query$', views.DomainsQuery, name='DomainsQuery'),
    url('^domains/Delete$', views.DomainsDelete, name='DomainsDelete'),
    url('^domains/Add$', views.DomainsAdd, name='DomainsAdd'),
    url('^domains/Update$', views.DomainsUpdate, name='DomainsUpdate'),
    url('^domains/UpdateStatus$', views.DomainsUpdateStatus, name='DomainsUpdateStatus'),
]
