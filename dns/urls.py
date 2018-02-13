from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url('^updaterecord$', views.UpdateRecord, name='UpdateRecord'),
    url('^cloudflare/index$', views.Index, name='Index'),
    url('^cloudflare/get_product_records$', views.GetProductRecords, name='GetProductRecords'),
    url('^cloudflare/get_zone_records$', views.GetZoneRecords, name='GetZoneRecords'),
    url('^cloudflare/update_records$', views.UpdateRecords, name='UpdateRecords'),
]
