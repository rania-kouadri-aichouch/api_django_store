from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product
from accounts.models import User


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'name', 'price', 'quantity',)
        read_only_fields = ['slug', 'type']

    def get_id(self, obj):
        return obj.product.id

    def get_name(self, obj):
        return obj.product.name

    def get_price(self, obj):
        return obj.product.price


class AddToCartSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_active=True))
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(required=False, min_value=1, initial=1)
    override = serializers.BooleanField(required=False, initial=False)

    def validate(self, attrs):
        if not Product.objects.filter(id=attrs['product'].id, qty_available__gte=0, is_available=True).exists():
            raise serializers.ValidationError({
                'message': 'this product is not available '
            })
        return super(AddToCartSerializer, self).validate(attrs)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'product', 'override',)


class SelectSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)

    class Meta:
        fields = ('product',)
