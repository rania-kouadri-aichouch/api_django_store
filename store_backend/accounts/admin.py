from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *

# Register your models here.
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_active', 'auth_provider', 'is_staff', 'is_superuser']
    list_filter = ['username', 'email']
    search_fields = ['username', 'email']


admin.site.register(Profile)
