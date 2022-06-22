from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content','user','product', 'created_at', 'updated_at']


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'comment', 'created_at', 'updated_at']
