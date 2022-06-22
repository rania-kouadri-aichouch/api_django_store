from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import models, serializers
from shared.permissions import IsAdminOrReadOnly


# Create your views here.

class ReplyToCommentAPIView(generics.CreateAPIView):
    serializer_class = serializers.ReplySerializer
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['user'] = request.user
            reply = serializer.save()
            return Response(
                data=self.serializer_class(instance=reply).data,
                status=status.HTTP_201_CREATED
            )



class GetAllCommentsOfProductAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.ProductCommentWithRepliesSerializer
    lookup_url_kwarg = 'slug'

    def get_queryset(self):
        product_slug = self.kwargs.get(self.lookup_url_kwarg)
        try:
            return models.Comment.objects.filter(product__slug=product_slug)
        except models.Comment.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        data = self.get_queryset()
        if data is None:
            return Response(
                data={
                    "detail": "Not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serialized_data = self.serializer_class(instance=data, many=True).data
        return Response(
            data=serialized_data,
            status=status.HTTP_200_OK
        )


class AddCommentToProductAPIView(generics.CreateAPIView):
    serializer_class = serializers.ProductCommentSerializer
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['user'] = request.user
            comment = serializer.save()
            return Response(
                data=self.serializer_class(instance=comment).data,
                status=status.HTTP_201_CREATED
            )

