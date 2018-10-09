# coding: utf8
from django.conf.urls import url, include
from django.urls import path, re_path 
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    re_path('^$', views.index, name='index'),
    re_path('^services$', views.Services, name='Services'),
    re_path('^project/Query$', views.ProjectQuery, name='ProjectQuery'),
    re_path('^project/UpdateStatus$', views.ProjectUpdateStatus, name='ProjectUpdateStatus'),
    re_path('^project/CheckServer$', views.ProjectCheckServer, name='ProjectCheckServer'),
    
    #域名监控
    re_path('^domains$', views.Domains, name='Domains'),
    re_path('^domains/getGroups$', views.GetGroups, name='GetGroups'),
    re_path('^domains/Query$', views.DomainsQuery, name='DomainsQuery'),
    re_path('^domains/Delete$', views.DomainsDelete, name='DomainsDelete'),
    re_path('^domains/Add$', views.DomainsAdd, name='DomainsAdd'),
    re_path('^domains/Update$', views.DomainsUpdate, name='DomainsUpdate'),
    re_path('^domains/UpdateStatus$', views.DomainsUpdateStatus, name='DomainsUpdateStatus'),
]
