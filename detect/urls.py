from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url('get_domains$', views.GetDomains, name='GetDomains'),
    url('send_telegram$', views.SendTelegram, name='SendTelegram'),
    #url('get_telegram_user_id$', views.GetTelegramUserId, name='GetTelegramUserId'),
]
