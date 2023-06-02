from rest_framework import authentication, generics, mixins
from scraped.models import EcommerceStore, LocalStore
from scraped.serializers import (
    EcommerceStoreSerializer,
    EcommerceStoreDetailSerializer,
    EcommerceStoreLocalStoresSerializer,
    LocalStoreSerializer,
    LocalStoreDetailSerializer,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class EcommerceStoreListAPIView(generics.ListAPIView):
    """List Api View for EcommerceStore."""

    serializer_class = EcommerceStoreSerializer
    queryset = EcommerceStore.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.order_by("-id")


ecommerce_store_list_view = EcommerceStoreListAPIView.as_view()


class EcommerceStoreDetailAPIView(generics.RetrieveAPIView):
    """Detail Api View for EcommerceStore."""

    queryset = EcommerceStore.objects.all()
    serializer_class = EcommerceStoreDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


ecommerce_store_detail_view = EcommerceStoreDetailAPIView.as_view()


class EcommerceStoreCreateAPIView(generics.CreateAPIView):
    """Create Api View for EcommerceStore."""

    queryset = EcommerceStore.objects.all()
    serializer_class = EcommerceStoreDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


ecommerce_store_create_view = EcommerceStoreCreateAPIView.as_view()


class EcommerceStoreUpdateAPIView(generics.UpdateAPIView):
    """Update Api View for EcommerceStore."""

    queryset = EcommerceStore.objects.all()
    serializer_class = EcommerceStoreDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


ecommerce_store_update_view = EcommerceStoreUpdateAPIView.as_view()


class EcommerceStoreDeleteAPIView(generics.DestroyAPIView):
    """Delete Api View for EcommerceStore."""

    queryset = EcommerceStore.objects.all()
    serializer_class = EcommerceStoreDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


ecommerce_store_delete_view = EcommerceStoreDeleteAPIView.as_view()


class EcommerceStoreLocalStoresAPIView(generics.RetrieveAPIView):
    """"""
    queryset = EcommerceStore.objects.all()
    serializer_class = EcommerceStoreLocalStoresSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


ecommerce_store_local_stores_view = EcommerceStoreLocalStoresAPIView.as_view()


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
