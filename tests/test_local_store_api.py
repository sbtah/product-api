"""
Tests for LocalStore related APIs
"""
import pytest
from django.urls import reverse
from rest_framework import status

from scraped.models import EcommerceStore, LocalStore
from scraped.serializers import (
    LocalStoreDetailSerializer,
    LocalStoreSerializer,
)

LOCAL_STORES_URL = reverse('scraped:local-store-list')
pytestmark = pytest.mark.django_db


class TestPublicLocalStoreApi:
    """
    Test unauthenticated API requests for LocalStore endpoints.
    """

    def test_authentication_required_for_list_endpoint(self, api_client):
        """
        Test that authentication is required to access
        LocalStore list endpoint.
        """

        res = api_client.get(LOCAL_STORES_URL)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


class TestPrivateLocalStoreApi:
    """
    Test authenticated API requests.
    """

    def test_get_local_stores(
            self,
            example_ecommerce_store,
            example_local_store,
            authenticated_client,
            create_example_local_stores
    ):
        """Test retrieving a list of LocalStores."""

        create_example_local_stores
        res = authenticated_client.get(LOCAL_STORES_URL)
        local_stores = LocalStore.objects.all().order_by('-id')
        serializer = LocalStoreSerializer(local_stores, many=True)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

