from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url('^$', views.Index, name='Index'),
    url('^get_servers_records$', views.GetServersRecords, name='GetServersRecords'),
]