from django.contrib import admin
from models import groups, domains, cdn_account_t
# Register your models here.

admin.site.register(groups)
admin.site.register(domains)
admin.site.register(cdn_account_t)