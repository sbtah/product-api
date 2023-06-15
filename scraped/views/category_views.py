from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from scraped.models import Category
from scraped.serializers.category_serializers import (
    CategoryDetailSerializer,
    CategorySerializer,
)


class CategoryListApiView(generics.ListAPIView):
    """List Api View for Category objects."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.order_by('-id')


category_list_view = CategoryListApiView.as_view()


class CategoryDetailAPIView(generics.RetrieveAPIView):
    """Detail Api view for Category object."""

    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


category_detail_view = CategoryDetailAPIView.as_view()
