from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from . import models, serializers

from cart.models import Cart, CartItem
from accounts.models import User
from products.models import Product
from django.core.exceptions import ValidationError, ObjectDoesNotExist

# Create your views here.
class AllOrdersViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    queryset = models.Order.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['get', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user',)



class CreateOrderAPIView(generics.CreateAPIView):
    serializer_class = serializers.OrderSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['user'] = request.user
            try:
                cart = Cart.objects.get(user=request.user)
                if len(cart.items.all()) < 1:
                    return Response(
                        data={
                            'message': 'Your cart is empty',
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                user = User.objects.get(id=serializer.validated_data['user'].id)
                order = models.Order.objects.create(
                    user=user,
                    payment_method=serializer.validated_data['payment_method'],
                )
                for item in cart.items.all():
                    item = CartItem.objects.get(id=item.id)
                    product = Product.objects.get(id=item.product.id)
                    if product.qty_available < item.quantity:
                        return Response(
                            data={
                                'Error': ValidationError(
                                    'The quantity of the product available is insufficient for this order'),
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    models.OrderItem.objects.create(
                        product=item.product,
                        order=order,
                        quantity=item.quantity
                    )
                    product.qty_available = product.qty_available - item.quantity
                    if product.qty_available < 1:
                        product.is_available = False
                    product.save()
                return Response(
                    data={
                        'message': 'Order created! '
                    },
                    status=status.HTTP_200_OK
                )
            except Cart.DoesNotExist:
                return Response(
                    data={
                        'message': 'Your cart is empty',
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
