from django.urls import path

from . import views

urlpatterns = [
    path('add-to-cart', views.AddToCartView.as_view(), name='Add to cart'),
    path('cart-details/<user_id>', views.CartDetailsView.as_view(), name='Cart details'),
    path('remove-from-cart', views.RemoveFromCartView.as_view(), name='Remove from cart'),
]