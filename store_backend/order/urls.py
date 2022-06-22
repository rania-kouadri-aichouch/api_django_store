from django.urls import path
from django.urls import include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('all', views.AllOrdersViewSet)


urlpatterns = [
    path('create', views.CreateOrderAPIView.as_view(), name='create-order'),
    path('', include(router.urls))
]
