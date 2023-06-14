from rest_framework import generics
from scraped.models import Category
from scraped.serializers.category_serializers import CategorySerializer, CategoryDetailSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


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
