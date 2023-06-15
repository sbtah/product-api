from rest_framework import generics
from scraped.models import EcommerceStore, LocalStore
from scraped.serializers.local_store_serializers import (
    LocalStoreSerializer,
    LocalStoreDetailSerializer,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class LocalStoreListAPIView(generics.ListAPIView):
    """List Api View for LocalStore."""

    serializer_class = LocalStoreSerializer
    queryset = LocalStore.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.order_by("-id")


local_store_list_view = LocalStoreListAPIView.as_view()


class LocalStoreDetailAPIView(generics.RetrieveAPIView):
    """Detail Api View for LocalStore."""

    queryset = LocalStore.objects.all()
    serializer_class = LocalStoreDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


local_store_detail_view = LocalStoreDetailAPIView.as_view()


class LocalStoreCreateAPIView(generics.CreateAPIView):
    """Create Api View for EcommerceStore."""

    queryset = LocalStore.objects.all()
    serializer_class = LocalStoreDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


local_store_create_view = LocalStoreCreateAPIView.as_view()


class LocalStoreUpdateAPIView(generics.UpdateAPIView):
    """Update Api View for LocalStore."""

    queryset = LocalStore.objects.all()
    serializer_class = LocalStoreDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


local_store_update_view = LocalStoreUpdateAPIView.as_view()


class LocalStoreDeleteAPIView(generics.DestroyAPIView):
    """Delete Api View for LocalStore."""

    queryset = LocalStore.objects.all()
    serializer_class = LocalStoreDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


local_store_delete_view = LocalStoreDeleteAPIView.as_view()
