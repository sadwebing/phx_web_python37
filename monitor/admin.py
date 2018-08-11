from django.contrib import admin
from models import project_t, minion_ip_t, minion_t, cdn_proj_t, project_authority_t
from models import telegram_domain_alert_t, telegram_ssl_alert_t, dns_authority_t, permission_t

admin.site.register(project_t)
admin.site.register(minion_ip_t)
admin.site.register(minion_t)
admin.site.register(cdn_proj_t)
admin.site.register(project_authority_t)
admin.site.register(telegram_domain_alert_t)
admin.site.register(telegram_ssl_alert_t)
admin.site.register(dns_authority_t)
admin.site.register(permission_t)