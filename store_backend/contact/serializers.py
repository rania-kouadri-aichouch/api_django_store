from rest_framework import serializers
from .models import Contact


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'number','is_seen', 'message', 'created_at', 'updated_at')


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    email = serializers.EmailField(max_length=100, allow_null=False, allow_blank=False)
    number = serializers.CharField(max_length=13, allow_null=True, allow_blank=False)
    message = serializers.CharField(max_length=100, allow_null=True, allow_blank=False, required=False)
    class Meta:
        fields = ('id', 'name', 'email', 'number','message', 'created_at', 'updated_at')

    def create(self, validated_data):

        contact = Contact.objects.create(
            name=validated_data.get('name'),
            email=validated_data.get('email'),
            number=validated_data.get('number'),
            is_seen=validated_data.get('is_seen'),
            message=validated_data.get('message'),
        )
        contact.save()

        return validated_data
    def validate(self, attrs):
        validated_data = super(ContactSerializer, self).validate(attrs)

        is_seen = attrs.get('is_seen', None)
        is_seen="False"
        validated_data['is_seen'] = is_seen

        return validated_data
