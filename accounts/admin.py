from django.contrib import admin
from accounts.models import UserProfile, user_project_authority_t
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
admin.site.register(user_project_authority_t)