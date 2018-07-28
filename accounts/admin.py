from django.contrib import admin
from models import UserProfile, telegram_chat_group_t, telegram_user_id_t
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin  

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = UserProfile
    #fk_name = 'user'
    max_num = 1
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline,]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(telegram_chat_group_t)
admin.site.register(telegram_user_id_t)
