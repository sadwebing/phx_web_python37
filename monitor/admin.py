from django.contrib import admin
from models import project_t, minion_ip_t, minion_t

admin.site.register(project_t)
admin.site.register(minion_ip_t)
admin.site.register(minion_t)