from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url('^services$', views.Services, name='Services'),
    url('^project/Query$', views.ProjectQuery, name='ProjectQuery'),
    url('^project/UpdateStatus$', views.ProjectUpdateStatus, name='ProjectUpdateStatus'),
    url('^project/CheckServer$', views.ProjectCheckServer, name='ProjectCheckServer'),
]
