from django.conf.urls import include, url
from django.urls import path, re_path 
from django.contrib import admin
from django.contrib import auth
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect
from accounts.views import home
from django.views.static import serve
from django.conf.urls.static import static
import accounts.urls, monitor.urls, dns.urls, detect.urls, saltstack.urls, servers.urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'phxweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    re_path(r'^home$', home),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/', include(accounts.urls)),
    re_path(r'^', include(monitor.urls)),
    re_path(r'^monitor/', include(monitor.urls)),
    re_path(r'^dns/', include(dns.urls)),
    re_path(r'^detect/', include(detect.urls)),
    re_path(r'^saltstack/', include(saltstack.urls)),
    re_path(r'^servers/', include(servers.urls)),

    re_path(r'^favicon$', lambda x: HttpResponseRedirect(settings.STATIC_URL+'images/favicon.ico')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
