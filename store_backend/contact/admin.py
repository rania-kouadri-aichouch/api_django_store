from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'number','message', 'created_at', 'updated_at']
    list_filter = ['email']
    search_fields = ['email']
