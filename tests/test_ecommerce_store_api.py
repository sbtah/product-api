"""
Tests for EcommerceStore related APIs
"""
import pytest
from django.urls import reverse
from rest_framework import status

from scraped.models import EcommerceStore, LocalStore
from scraped.serializers import (
    EcommerceStoreDetailSerializer,
    EcommerceStoreSerializer,
    EcommerceStoreLocalStoresSerializer,
)

ECOMMERCE_STORES_URL = reverse('scraped:store-list')
ECOMMERCE_STORE_CREATE_URL = reverse('scraped:store-create')
pytestmark = pytest.mark.django_db


def detail_url(ecommerce_store_id):
    """Create and return EcommerceStore detail url."""
    return reverse('scraped:store-detail', args=[ecommerce_store_id])


def update_url(ecommerce_store_id):
    """Create and return EcommerceStore update url."""
    return reverse('scraped:store-update', args=[ecommerce_store_id])


def delete_url(ecommerce_store_id):
    """Create and return EcommerceStore delete url."""
    return reverse('scraped:store-delete', args=[ecommerce_store_id])


def list_children_stores_url(ecommerce_store_id):
    """Create and return EcommerceStore list all LocalStores url."""
    return reverse('scraped:children-stores', args=[ecommerce_store_id])


class TestPublicEcommerceStoreApi:
    """
    Test unauthenticated API requests.
    """

    def test_authentication_required_for_list_endpoint(self, api_client):
        """
        Test that authentication is required to access
        EcommerceStore list endpoint.
        """

        res = api_client.get(ECOMMERCE_STORES_URL)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authentication_required_for_detail_endpoint(
            self,
            api_client,
            example_ecommerce_store,
    ):
        """
        Test that authentication is required to access
        EcommerceStore detail endpoint.
        """
        e_store = example_ecommerce_store
        url = delete_url(e_store.id)
        res = api_client.get(url)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authentication_required_for_create_endpoint(self, api_client):
        """
        Test that authentication is required to access
        EcommerceStore create endpoint.
        """
        res = api_client.post(ECOMMERCE_STORE_CREATE_URL)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authentication_required_for_update_endpoint(
            self,
            api_client,
            example_ecommerce_store,
    ):
        """
        Test that authentication is required to access
        EcommerceStore update endpoint.
        """
        e_store = example_ecommerce_store
        url = update_url(e_store.id)
        res = api_client.patch(url)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        res_2 = api_client.put(url)
        assert res_2.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authentication_required_for_delete_endpoint(
            self,
            api_client,
            example_ecommerce_store,
    ):
        """
        Test that authentication is required to access
        EcommerceStore delete endpoint.
        """
        e_store = example_ecommerce_store
        url = detail_url(e_store.id)
        res = api_client.delete(url)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


class TestPrivateEcommerceStoreApi:
    """
    Test authenticated API requests.
    """

    def test_get_ecommerce_stores(
            self,
            example_ecommerce_store,
            authenticated_client,
    ):
        """Test retrieving a list of EcommerceStores."""

        for _ in range(3):
            example_ecommerce_store
        res = authenticated_client.get(ECOMMERCE_STORES_URL)
        e_stores = EcommerceStore.objects.all().order_by('-id')
        serializer = EcommerceStoreSerializer(e_stores, many=True)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_get_ecommerce_store(
            self,
            example_ecommerce_store,
            authenticated_client,
    ):
        """Test get EcommerceStore detail."""

        e_store = example_ecommerce_store
        url = detail_url(e_store.id)
        res = authenticated_client.get(url)
        serializer = EcommerceStoreDetailSerializer(e_store)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_create_ecommerce_store(self, authenticated_client):
        """Test creating an EcommerceStore."""

        payload = {
            'name': 'Test Store',
            'domain': 'test-store.com',
            'discovery_url': 'https://test-store.com/'
        }
        res = authenticated_client.post(ECOMMERCE_STORE_CREATE_URL, payload)
        assert res.status_code == status.HTTP_201_CREATED
        e_store = EcommerceStore.objects.first()
        for k, v in payload.items():
            assert getattr(e_store, k) == v

    def test_perform_partial_update_ecommerce_store(
            self,
            authenticated_client,
            example_ecommerce_store,
    ):
        """Test partial update on EcommerceStore."""

        e_store = example_ecommerce_store
        payload = {'name': 'New Store Name'}
        url = update_url(e_store.id)
        res = authenticated_client.patch(url, payload)

        assert res.status_code == status.HTTP_200_OK
        e_store.refresh_from_db()
        assert e_store.name == payload['name']

    def test_perform_full_update_ecommerce_store(
            self,
            authenticated_client,
            example_ecommerce_store,
    ):
        """Test full update on EcommerceStore."""

        e_store = example_ecommerce_store
        payload = {
            'name': 'This is New Name',
            'domain': 'this-is-new.com',
            'discovery_url': 'https://this-is-new.com/',
            'package_name': 'this_new',
            'module_name': 'this_new',
            'class_name': 'ThisNew',
            'last_scrape_start': 1,
            'last_scrape_end': 2,
            'is_active': False,
            'is_monitored': False,
        }
        url = update_url(e_store.id)
        res = authenticated_client.put(url, payload)

        assert res.status_code == status.HTTP_200_OK
        e_store.refresh_from_db()
        for k, v in payload.items():
            assert getattr(e_store, k) == v

    def test_delete_ecommerce_store(
            self,
            authenticated_client,
            example_ecommerce_store,
    ):
        """Test deleting EcommerceStore successful."""

        e_store = example_ecommerce_store
        url = delete_url(e_store.id)
        res = authenticated_client.delete(url)

        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert EcommerceStore.objects.filter(id=e_store.id).exists() is False

    # def test_list_all_local_stores(
    #     self,
    #     authenticated_client,
    #     example_ecommerce_store,
    #     create_example_local_stores,
    # ):
    #     """Test listing all children LocalStores for EcommerceStore."""
    #
    #     e_store = example_ecommerce_store
    #     create_example_local_stores
    #     local_stores = LocalStore.objects.filter(parent_store=e_store)
    #     print(local_stores)
    #     serializer = EcommerceStoreLocalStoresSerializer(local_stores, many=True)
    #     url = list_children_stores_url(e_store.id)
    #     res = authenticated_client.get(url)
    #     print(res.data)
    #     print(serializer.data)
    #     assert serializer.data in res.data
