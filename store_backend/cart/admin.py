from django.contrib import admin
from .models import Cart, CartItem


# Register your models here.
class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity']
