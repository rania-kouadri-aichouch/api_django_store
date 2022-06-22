from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views




urlpatterns = [
    path('get/<slug>', views.GetAllCommentsOfProductAPIView.as_view(), name='get-comments-with-replies'),
    path('create', views.AddCommentToProductAPIView.as_view(), name='add-new-comment'),
    path('replies/create', views.ReplyToCommentAPIView.as_view(), name='reply-to-comment'),
]
