from rest_framework import serializers
from rest_framework_simplejwt import serializers as jwt_serializers
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Profile


class CustomTokenObtainPairSerializer(jwt_serializers.TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        token['auth_provider'] = user.auth_provider
        try:
            token['image'] = str(user.profile.image)
            token['full_name'] = str(user.profile.full_name)
            return token
        except ObjectDoesNotExist:
            return token


class SocialAuthSerializer(serializers.ModelSerializer):
    """
        Social Auth serializer
    """
    image = serializers.URLField()
    full_name = serializers.CharField(max_length=255, allow_null=False, allow_blank=False)


    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'image', 'auth_provider',)
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        if attrs['auth_provider'] == 'email':
            raise serializers.ValidationError({
                'auth_provider': 'Invalid social auth',
            })
        return super(SocialAuthSerializer, self).validate(attrs=attrs)

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        auth_provider = validated_data['auth_provider']

        user = User.objects.create_user(
            username=username,
            email=email,
            auth_provider=auth_provider,
            is_active=True
        )

        profile = Profile.objects.create(
            user=user,
            full_name=validated_data['full_name'],

        )

        profile.image = validated_data['image']
        profile.save()
        return user


class RegistrationSerializer(serializers.ModelSerializer):
    """
        For Creating a new user. Email, username, and password are required.
        Returns a JSON web token.
    """
    full_name = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(min_length=6, write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ('email', 'username', 'full_name', 'password', 'auth_provider')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            auth_provider=validated_data['auth_provider'],
            password=validated_data['password']
        )
        Profile.objects.create(
            user=user,
            full_name=validated_data['full_name'],

        )
        return user


class EditRolesSerializer(serializers.Serializer):
    """
        Serializer for roles edit endpoint.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_active=True))
    is_editor = serializers.BooleanField(default=False)
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)

    class Meta:
        fields = ('user', 'is_staff', 'is_superuser', 'is_staff')


class EditPasswordSerializer(serializers.Serializer):
    """
        Serializer for password edit endpoint.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_active=True))
    new_password = serializers.CharField(required=True)

    class Meta:
        fields = ('user', 'new_password',)


class UpdatePasswordSerializer(EditPasswordSerializer):
    """
        Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)

    class Meta:
        fields = ('user', 'old_password', 'new_password',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'image', 'full_name',)

    def to_representation(self, obj):
        representation = super().to_representation(obj)

        if str(obj.image).startswith("https://") or str(obj.image).startswith("http://"):
            representation['image'] = str(obj.image)
        else:
            request = self.context.get('request')
            image = obj.image.url
            representation['image'] = request.build_absolute_uri(image)
        return representation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'auth_provider',
                  'created_at', 'updated_at')


class RequestResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=6, required=True)

    class Meta:
        fields = "__all__"


class ProceedResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        fields = "__all__"


class ResendEmailActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=6, required=True)

    class Meta:
        fields = "__all__"
