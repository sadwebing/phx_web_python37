from django.contrib import admin
from models import cf_account, dnspod_account, domain_info, alter_history
# Register your models here.

admin.site.register(cf_account)
admin.site.register(domain_info)
admin.site.register(alter_history)
admin.site.register(dnspod_account)