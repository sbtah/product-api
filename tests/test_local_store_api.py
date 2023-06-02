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

LOCAL_STORE_LIST_URL = reverse('scraped:local-store-list')
# LOCAL_STORE_CREATE_URL = reverse('scraped:local-store-create')
pytestmark = pytest.mark.django_db


def detail_url(local_store_id):
    """Create and return LocalStore detail url."""
    return reverse('scraped:local-store-detail', args=[local_store_id])


class TestPublicLocalStoreApi:
    """
    Test unauthenticated API requests for LocalStore endpoints.
    """

    def test_authentication_required_for_list_endpoint(self, api_client):
        """
        Test that authentication is required to access
        LocalStore list endpoint.
        """

        res = api_client.get(LOCAL_STORE_LIST_URL)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authentication_required_for_detail_endpoint(
            self,
            api_client,
            example_local_store,
    ):
        """
        Test that authentication is required to access
        LocalStore detail endpoint.
        """

        local_store = example_local_store
        url = detail_url(local_store.id)
        res = api_client.get(url)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    # def test_authentication_required_for_create_endpoint(self, api_client):
    #     """
    #     Test that authentication is required to access
    #     LocalStore create endpoint.
    #     """
    #
    #     res = api_client.get(LOCAL_STORE_CREATE_URL)
    #     assert res.status_code == status.HTTP_401_UNAUTHORIZED


class TestPrivateLocalStoreApi:
    """
    Test authenticated API requests.
    """

    def test_get_local_stores(
            self,
            create_example_local_stores,
            authenticated_client,
    ):
        """Test retrieving a list of LocalStores."""

        create_example_local_stores
        res = authenticated_client.get(LOCAL_STORE_LIST_URL)
        local_stores = LocalStore.objects.all().order_by('-id')
        serializer = LocalStoreSerializer(local_stores, many=True)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_get_local_store(self, example_local_store, authenticated_client):
        """Test get LocalStore detail."""

        local_store = example_local_store
        url = detail_url(local_store.id)
        res = authenticated_client.get(url)
        serializer = LocalStoreDetailSerializer(local_store)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data
