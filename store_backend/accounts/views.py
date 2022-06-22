import jwt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, filters, viewsets, permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from .serializers import *
from .models import User, Profile

# Create your views here.
class DefaultPagination(PageNumberPagination):
    """
        The pagination class for our views
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 300


class AllUsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-created_at')
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = DefaultPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ['username', 'email']
    filter_fields = ('username', 'email')


class TokenObtainPairView(jwt_views.TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = User.objects.filter(email=request.data['email'])
        google_user = User.objects.exclude(auth_provider='email').filter(email=request.data['email'])

        if google_user.exists():
            return Response(
                data={
                    "message": "User already registered with google"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.exists():
            user = user.get(email=request.data['email'])
            if user.check_password(request.data['password']):
                if user.is_active:
                    serializer.is_valid()
                    return Response(
                        data=serializer.validated_data,
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        data={
                            "message": "There's no active account with this credentials"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    data={
                        "message": "Wrong password"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                data={
                    "message": "User not found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        google_user = User.objects.exclude(auth_provider='email').filter(email=request.data['email'])

        if google_user.exists():
            return Response(
                data={
                    "message": "User already registered with google"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:

            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            token = RefreshToken.for_user(user=user).access_token
            return Response(
                data={
                    'message': 'Your account has been created successfully!'
                },
                status=status.HTTP_200_OK,
            )

        except Exception as ex:
            if serializer.errors.get('email'):
                return Response(
                    data={
                        "message": "There is already a user registered with this email."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            raise ex



class CreateProfileAPIView(APIView):
    serializer_class = ProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(
            data={
                'user_id': data.user.id,
                'profile_id': data.id,
                'email': data.user.email,
                'image': str(data.image),
                'family_name': data.family_name
            },
            status=status.HTTP_200_OK
        )


class ProfileDetailView(generics.GenericAPIView):
    serializer_class = ProfileSerializer

    def get(self, request, user_id, *args, **kwargs):
        try:
            user_profile = Profile.objects.get(user__id=user_id)
            return Response(
                data={
                    'Message': 'User profile fetched successfully',
                    'User': ProfileSerializer(context={'request': request}, instance=user_profile).data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as ex:
            return Response(
                data={
                    'Message': 'User does not exists',
                    'Error': str(ex)
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

    def patch(self, request, user_id, *args, **kwargs):
        user_profile = Profile.objects.get(user__id=user_id)
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.update(instance=user_profile, validated_data=serializer.validated_data)

        return Response(
            data={
                'message': 'Profile updated !',
                'user_id': ProfileSerializer(context={'request': request}, instance=user_profile).data['user'],
                'profile_id': ProfileSerializer(context={'request': request}, instance=user_profile).data['id'],
                'email': data.user.email,
                'image': ProfileSerializer(context={'request': request}, instance=user_profile).data['image'],
                'family_name': ProfileSerializer(context={'request': request}, instance=user_profile).data[
                    'family_name'],

            },
            status=status.HTTP_200_OK
        )


class UpdatePasswordView(generics.GenericAPIView):
    serializer_class = UpdatePasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            user = User.objects.get(id=user.id)
            if not user.check_password(serializer.data.get("old_password")):
                return Response(
                    data={"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(serializer.data.get("new_password"))
            user.save()

            return Response(
                data={
                    'message': 'Password updated successfully',
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocialAuthView(APIView):
    serializer_class = SocialAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user = User.objects.exclude(auth_provider='email').filter(email=request.data['email'])
        email_user = User.objects.exclude(auth_provider='google').filter(email=request.data['email'])

        if user.exists():
            user = user.get(email=request.data['email'])
            refresh_token = CustomTokenObtainPairSerializer.get_token(user)
            return Response(
                data={
                    'Message': 'User already exists !',
                    'refresh': str(refresh_token),
                    'access': str(refresh_token.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            if email_user:
                    return Response(
                        data={
                            "message": "this account is not registered with google"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                        )
            else:
              if serializer.is_valid(raise_exception=True):
                  user = serializer.save()
                  refresh_token = CustomTokenObtainPairSerializer.get_token(user)
                  return Response(
                      data={
                          'Message': 'User created successfully !',
                          'refresh': str(refresh_token),
                          'access': str(refresh_token.access_token),
                      },
                      status=status.HTTP_200_OK
                  )
              else:
                  return Response(
                      data=serializer.errors,
                      status=status.HTTP_400_BAD_REQUEST
                  )


class EditUserRoles(generics.GenericAPIView):
    """
        Handles editing user's roles
    """
    serializer_class = EditRolesSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['patch']

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')
            is_editor = serializer.validated_data.get('is_editor')
            is_staff = serializer.validated_data.get('is_staff')
            is_superuser = serializer.validated_data.get('is_superuser')
            user.is_editor = is_editor
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()
            return Response(
                data={
                    'Message': 'Roles edited successfully',
                },
                status=status.HTTP_200_OK
            )
