from rest_framework import serializers
from . import models
from products.models import Product


class ProductCommentSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = models.Comment
        fields = ('id', 'user', 'product', 'content',  'created_at', 'updated_at')
        read_only_fields = ('user', 'product')

    def to_representation(self, instance):
        representation = super(ProductCommentSerializer, self).to_representation(instance)
        representation['user'] = {
            "id": instance.user.id,
            "username": instance.user.username,
            "picture": instance.user.profile.image,
            "is_staff": instance.user.is_staff
        }
        return representation




class ReplySerializer(serializers.ModelSerializer):
    comment = serializers.PrimaryKeyRelatedField(queryset=models.Comment.objects.all())
    class Meta:
        model = models.Reply
        fields = ('id', 'user', 'comment', 'content', 'created_at', 'updated_at')
        read_only_fields = ('user',)

    def to_representation(self, instance):
        representation = super(ReplySerializer, self).to_representation(instance)
        representation['user'] = {
          "id": instance.user.id,
          "username": instance.user.username,
          "picture": instance.user.profile.image,
          "is_staff": instance.user.is_staff

        }
        return representation


class ProductCommentWithRepliesSerializer(ProductCommentSerializer):
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = models.Comment
        fields = ('id', 'user', 'content', 'image', 'replies', 'created_at', 'updated_at')
