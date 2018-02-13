from django.conf.urls import include, url
from django.contrib import admin
from django.contrib import auth
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect
from accounts.views import home

urlpatterns = [
    # Examples:
    # url(r'^$', 'phxweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^home$', home),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^', include('monitor.urls')),
    url(r'^monitor/', include('monitor.urls')),
    url(r'^dns/', include('dns.urls')),

    url(r'^favicon$', lambda x: HttpResponseRedirect(settings.STATIC_URL+'images/favicon.ico')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
