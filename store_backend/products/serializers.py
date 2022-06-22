from rest_framework import serializers
from .models import *



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name', 'slug', 'price', 'qty_available', 'is_available','categories', 'created_at', 'updated_at')


    def to_representation(self, instance):
        categories = CategorySerializer(read_only=True, many=True)
        representation = super(ProductSerializer, self).to_representation(instance)
        representation['categories'] = []
        for entry in instance.categories.all():
            category = CategorySerializer(entry).data
            representation['categories'].append(category)
        return representation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name', 'slug', 'created_at', 'updated_at')
