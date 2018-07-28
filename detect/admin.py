from django.contrib import admin
from models import groups, domains, cdn_account_t, telegram_chat_group_t, telegram_user_id_t
# Register your models here.

admin.site.register(groups)
admin.site.register(domains)
admin.site.register(cdn_account_t)

admin.site.register(telegram_chat_group_t)
admin.site.register(telegram_user_id_t)