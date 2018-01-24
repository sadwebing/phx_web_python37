from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url('^logout$', views.logout),
    url('^login$', views.login),
]
