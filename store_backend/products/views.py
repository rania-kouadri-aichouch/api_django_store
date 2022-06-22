from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from accounts.models import User


# Create your views here.
class DefaultPagination(PageNumberPagination):
    """
        The pagination class for our views
    """
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 300


class ProductsViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Product.objects.all()
    pagination_class = DefaultPagination

    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ['name', ]
    filter_fields = ('categories',)


class GetProductDetailsView(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request, slug, *args, **kwargs):
        serializer = self.get_serializer()
        product = Product.objects.get(slug=slug)
        return Response(
            data=ProductSerializer(instance=product, context={'request': request}).data,
            status=status.HTTP_200_OK
        )


class CategoryViewSet(viewsets.ModelViewSet):
    """
        Handles listing, creating, updating, and deleting categories from the system
    """
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Category.objects.all()
    pagination_class = DefaultPagination
