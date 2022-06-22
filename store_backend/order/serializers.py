from rest_framework import serializers
from .models import *
from cart.models import Cart, CartItem
from products.models import Product


class ChangeStatusSerializer(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=True)
    status = serializers.CharField(
        required=True,
        max_length=15
    )

    class Meta:
        fields = ('order', 'status')



class ItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    quantity_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'price', 'quantity', 'quantity_price')

    def get_product_name(self, obj):
        return obj.product.name

    def get_quantity_price(self, obj):
        return obj.get_cost()

class OrderSerializer(serializers.ModelSerializer):
    items = items = ItemSerializer(many=True, read_only=True)
    total_cost = serializers.SerializerMethodField(read_only=True)
    total_items_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'payment_method', 'items', 'total_cost', 'total_items_count', 'status', 'created_at',
                  'updated_at',)
        read_only_fields = ['user', 'status']


    def get_total_cost(self, obj):
        return obj.get_items_cost()

    def get_total_items_count(self, obj):
        return obj.get_total_items_count()


    def to_representation(self, instance):
        representation = super(OrderSerializer, self).to_representation(instance)
        representation['user'] = {
            "id": instance.user.id,
            "username": instance.user.username,
        }
        return representation
