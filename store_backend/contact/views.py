from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from . import models, serializers
from rest_framework import viewsets, permissions, generics, status
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ContactsSerializer
    queryset = models.Contact.objects.all().order_by('-created_at')
    #pagination_class = StandardResultsSetPagination
    http_method_names = ['get','patch', 'delete']

class CreateContactAPIView(generics.CreateAPIView):
    serializer_class = serializers.ContactSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            serializer.create(validated_data)
            return Response(
                data={
                    "message": "message created."
                },
                status=status.HTTP_201_CREATED
            )
