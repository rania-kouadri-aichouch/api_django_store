from django.contrib import admin
from .models import Category, Product


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'qty_available', 'is_available', 'created_at', 'updated_at']
    list_filter = ['qty_available', 'is_available', 'created_at', 'updated_at']
    list_editable = ['price', 'qty_available', 'is_available']
