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
LOCAL_STORE_CREATE_URL = reverse('scraped:local-store-create')
pytestmark = pytest.mark.django_db


def detail_url(local_store_id):
    """Create and return LocalStore detail url."""
    return reverse('scraped:local-store-detail', args=[local_store_id])


def update_url(local_store_id):
    """Create and return LocalStore update url."""
    return reverse('scraped:local-store-update', args=[local_store_id])


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

    def test_authentication_required_for_create_endpoint(self, api_client):
        """
        Test that authentication is required to access
        LocalStore create endpoint.
        """

        res = api_client.get(LOCAL_STORE_CREATE_URL)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authentication_required_for_update_endpoint(
            self,
            api_client,
            example_local_store,
    ):
        """
        Test that authentication is required to access
        LocalStore update endpoint.
        """

        local_store = example_local_store
        url = update_url(local_store.id)
        res = api_client.patch(url)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        res_2 = api_client.put(url)
        assert res_2.status_code == status.HTTP_401_UNAUTHORIZED


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

    def test_create_local_store(
            self,
            example_ecommerce_store,
            authenticated_client,
    ):
        """Test creating a LocalStore."""

        e_store = example_ecommerce_store
        payload = {
            'parent_store': e_store.id,
            'name': 'New York',
            'scraped_id': 1,
            'is_active': True,
        }
        res = authenticated_client.post(LOCAL_STORE_CREATE_URL, payload)
        assert res.status_code == status.HTTP_201_CREATED
        local_store = LocalStore.objects.first()
        assert local_store.name == payload['name']
        assert local_store.scraped_id == payload['scraped_id']
        assert local_store.is_active == payload['is_active']
        assert local_store.parent_store == e_store

    def test_perform_partial_update_local_store(
            self,
            example_local_store,
            authenticated_client,
    ):
        """Test partial update on LocalStore."""

        local_store = example_local_store
        payload = {
            'name': 'New York Xtra'
        }
        url = update_url(local_store.id)
        res = authenticated_client.patch(url, payload)

        assert res.status_code == status.HTTP_200_OK
        local_store.refresh_from_db()
        assert local_store.name == payload['name']

    def test_perform_full_update_local_store(
            self,
            example_local_store,
            example_ecommerce_store_2,
            authenticated_client,
    ):
        """Test full update on LocalStore."""

        e_store = example_ecommerce_store_2
        local_store = example_local_store
        payload = {
            "id": 1,
            "name": "New York 315",
            "parent_store": e_store.id,
            "scraped_id": 222,
            "url": "http://www.new-url.com/",
            "api_url": "",
            'created': 1,
            "last_scrape_start": 0,
            "last_scrape_end": 0,
            "is_active": True,
            "is_monitored": True,
        }
        url = update_url(local_store.id)
        res = authenticated_client.put(url, payload)
        assert res.status_code == status.HTTP_200_OK
        local_store.refresh_from_db()
        assert local_store.parent_store == e_store
        assert local_store.name == payload['name']
        assert local_store.scraped_id == payload['scraped_id']
        assert local_store.url == payload['url']
        assert local_store.api_url == payload['api_url']
        assert local_store.created == payload['created']
        assert local_store.last_scrape_start == payload['last_scrape_start']
        assert local_store.last_scrape_end == payload['last_scrape_end']
        assert local_store.is_active == payload['is_active']
        assert local_store.is_monitored == payload['is_monitored']
