from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views
from . import nginx
from . import httpdns

urlpatterns = [
    url('^getDns$', httpdns.GetDns, name='GetDns'),
    url('^updaterecord$', views.UpdateRecord, name='UpdateRecord'),
    
    #cloudflare
    url('^cloudflare/index$', views.Index, name='Index'),
    url('^cloudflare/get_product_records$', views.GetProductRecords, name='GetProductRecords'),
    url('^cloudflare/get_zone_records$', views.GetZoneRecords, name='GetZoneRecords'),
    url('^cloudflare/update_records$', views.UpdateRecords, name='UpdateRecords'),
    url('^cloudflare/update_api_route$', views.UpdateApiRoute, name='UpdateApiRoute'),
    url('^cloudflare/get_api_route$', views.GetApiRoute, name='GetApiRoute'),

    #dnspod
    url('^dnspod/index$', views.DndpodIndex, name='DndpodIndex'),
    url('^dnspod/get_product_records$', views.GetDnspodProductRecords, name='GetDnspodProductRecords'),
    url('^dnspod/get_zone_records$', views.GetDnspodZoneRecords, name='GetDnspodZoneRecords'),
    url('^dnspod/update_records$', views.UpdateDnspodRecords, name='UpdateDnspodRecords'),
    url('^dnspod/delete_records$', views.DeleteDnspodRecords, name='DeleteDnspodRecords'),
    
    #config nginx
    url('^nginx$', nginx.Nginx, name='Nginx'),

]