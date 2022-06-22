from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('manage/all', AllUsersViewSet)

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh', TokenRefreshView.as_view(), name="token_refresh"),
    path('register', RegistrationAPIView.as_view(), name="register"),
    path('social-auth', SocialAuthView.as_view(), name='social-auth'),
    path('profile/new', CreateProfileAPIView.as_view(), name='create-profile'),
    path('profile/<user_id>', ProfileDetailView.as_view(), name='profile-detail'),
    path('password/update', UpdatePasswordView.as_view(), name='change-password'),
    path('roles/edit', EditUserRoles.as_view(), name='edit-roles'),
    path('', include(router.urls)),
]
