

'''
Tests for EcommerceStore related APIs
'''
import pytest
from django.urls import reverse
from rest_framework import status

from scraped.models import EcommerceStore
from scraped.serializers import (
    EcommerceStoreDetailSerializer,
    EcommerceStoreSerializer,
)


ECOMMERCE_STORES_URL = reverse('scraped:store-list')
ECOMMERCE_STORE_CREATE_URL = reverse('scraped:store-create')
pytestmark = pytest.mark.django_db


def detail_url(ecommerce_store_id):
    '''Create and return EcommerceStore detail url.'''
    return reverse('scraped:store-detail', args=[ecommerce_store_id])

def create_url(ecommerce_store_id):
    '''Create and returl EcommerceStore update url.'''
    return reverse('scraped:store-update', args=[ecommerce_store_id])


class TestPublicEcommerceStoreApi:
    '''
    Test unauthenticated API requests.
    '''

    def test_authentication_required(self, api_client):
        '''Test that authentication is required to access API.'''

        res = api_client.get(ECOMMERCE_STORES_URL)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


class TestPrivateEcommerceStoreApi:
    '''
    Test authenticated API requests.
    '''

    def test_get_ecommerce_stores(
        self,
        example_ecommerce_store,
        authenticated_client,
    ):
        '''Test retrieving a list of EcommerceStores.'''

        for _ in range(3):
            example_ecommerce_store
        res = authenticated_client.get(ECOMMERCE_STORES_URL)
        recipes = EcommerceStore.objects.all().order_by("-id")
        serializer = EcommerceStoreSerializer(recipes, many=True)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_get_ecommerce_store(
        self,
        example_ecommerce_store,
        authenticated_client,
    ):
        '''Test get EcommerceStore detail.'''

        e_store = example_ecommerce_store
        url = detail_url(e_store.id)
        res = authenticated_client.get(url)
        serializer = EcommerceStoreDetailSerializer(e_store)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data


    def test_create_ecommerce_store(self, authenticated_client):
        '''Test creating an EcommerceStore.'''

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

    def test_perform_partial_update(
            self,
            authenticated_client,
            example_ecommerce_store,
        ):
        '''Test partial update on EcommerceStore.'''

        e_store = example_ecommerce_store
        payload = {"name": "New Store Name"}
        url = create_url(e_store.id)
        res = authenticated_client.patch(url, payload)

        assert res.status_code == status.HTTP_200_OK
        e_store.refresh_from_db()
        assert e_store.name == payload["name"]
