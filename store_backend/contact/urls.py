from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'contact'

router = DefaultRouter()
router.register('', views.ContactViewSet)

urlpatterns = [
    path('create/', views.CreateContactAPIView.as_view(), name='create'),
    path('', include(router.urls)),
]
