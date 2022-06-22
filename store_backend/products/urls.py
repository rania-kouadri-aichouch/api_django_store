from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductsViewSet)
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('details/products/<slug>', views.GetProductDetailsView.as_view(), name='product-details'),
]
