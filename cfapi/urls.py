from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url('^updaterecord$', views.UpdateRecord, name='UpdateRecord'),
]
