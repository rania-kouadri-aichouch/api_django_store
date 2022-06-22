import products.models as models
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response

from accounts.models import User

from . import serializers
from .models import Cart, CartItem
from products.models import Product


# Create your views here.
class AddToCartView(generics.GenericAPIView):
    """
        Allow users to add items in their cart.
    """
    serializer_class = serializers.AddToCartSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = User.objects.get(id=serializer.validated_data['user'].id)
            product = models.Product.objects.get(id=serializer.validated_data['product'].id)
            override = serializer.validated_data['override']
            cart = Cart.objects.filter(user=user)
            if not cart.exists():
                cart = Cart.objects.create(
                    user=user
                )
            else:
                cart = Cart.objects.get(user=user)
                item = CartItem.objects.filter(cart=cart, product=product)
                if item.exists():
                    item = item.get(cart=cart, product=product)
                    if override:
                        item.quantity = serializer.validated_data['quantity']
                        item.save()
                    else:
                        item.quantity += serializer.validated_data['quantity']
                        item.save()
                    return Response(
                        data={
                            "Message": "Product in your cart updated !",
                        },
                        status=status.HTTP_201_CREATED
                    )

            item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=serializer.validated_data['quantity']
            )
            cart.items.add(item)
            return Response(
                data={
                    "Message": "Product added to your cart !",
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data={
                    'message': serializer.errors.get('message')[0]
                },
                status=status.HTTP_200_OK
            )

class RemoveFromCartView(generics.CreateAPIView):
    serializer_class = serializers.SelectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            product = serializer.validated_data.get('product')
            product = Product.objects.get(id=product.id)
            cart = Cart.objects.filter(user=user)
            if not cart.exists():
                return Response(
                    data={
                        "Message": "This user have no cart !",
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            try:
               cart = Cart.objects.get(user=user)
               item = CartItem.objects.get(cart=cart, product=product)
               item.delete()
            except CartItem.DoesNotExist:
                return Response(
                    data={
                        'message': 'product is not in your cart',
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                data={
                    "Message": "Product removed from your cart !",
                },
                status=status.HTTP_200_OK
            )


class CartDetailsView(generics.RetrieveAPIView):
    """
        Display cart content.
    """

    def get(self, request, user_id, *args, **kwargs):
        user = User.objects.filter(id=user_id)
        if not user.exists():
            return Response(
                data={
                    "Message": "There\'s no user with this id !",
                },
                status=status.HTTP_404_NOT_FOUND
            )
        user = User.objects.get(id=user_id)
        cart = Cart.objects.filter(user=user)
        if not cart.exists():
            return Response(
                data={
                    "cart": [],
                },
                status=status.HTTP_200_OK
            )
        cart = Cart.objects.get(user=user)
        return Response(
            data={
                'id': cart.id,
                'cart': serializers.ItemSerializer(instance=cart.items, many=True).data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, user_id, *args, **kwargs):
        user = User.objects.filter(id=user_id)
        if not user.exists():
            return Response(
                data={
                    "Message": "There\'s no user with this id !",
                },
                status=status.HTTP_404_NOT_FOUND
            )
        user = User.objects.get(id=user_id)
        cart = Cart.objects.filter(user=user)
        if not cart.exists():
            return Response(
                data={
                    "message": "The cart is already empty !",
                    "cart": []
                },
                status=status.HTTP_200_OK
            )
        cart = Cart.objects.get(user=user)
        cart.delete()
        return Response(
            data={
                "message": "The cart has been emptied !",
                "cart": []
            },
            status=status.HTTP_200_OK
        )
