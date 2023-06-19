"""
Tests for Category related APIs
"""
import pytest
from django.urls import reverse
from rest_framework import status

from scraped.models import Category, EcommerceStore
from scraped.serializers.category_serializers import (
    CategoryDetailSerializer,
    CategorySerializer,
)


CATEGORY_LIST_URL = reverse('scraped:category-list')
CATEGORY_CREATE_URL = reverse('scraped:category-create')
pytestmark = pytest.mark.django_db


def detail_url(category_id):
    """Create and return Category detail url."""
    return reverse('scraped:category-detail', args=[category_id])


class TestPublicCategoryApi:
    """
    Test unauthenticated API requests for Category endpoints.
    """

    def test_authentication_required_for_list_endpoints(self, api_client):
        """
        Test that authentication is required to access Category list endpoint.
        """

        res = api_client.get(CATEGORY_LIST_URL)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authentication_required_for_detail_endpoint(
            self,
            api_client,
            example_category,
    ):
        """
        Test that authentication is required to access
        Category detail endpoint.
        """

        category = example_category
        url = detail_url(category.id)
        res = api_client.get(url)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authentication_is_required_for_create_endpoint(self, api_client):
        """
        Test that authentication is required to access
        Category endpoint.
        """
        res = api_client.post(CATEGORY_CREATE_URL)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED

class TestPrivateCategoryApi:
    """
    Test authenticated API requests for Category endpoints.
    """

    def test_get_categories(
            self,
            create_example_categories,
            authenticated_client,
    ):
        """Test retrieving a list of Category objects."""

        create_example_categories
        res = authenticated_client.get(CATEGORY_LIST_URL)
        categories = Category.objects.all().order_by('-id')
        serializer = CategorySerializer(categories, many=True)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_get_category(self, example_category, authenticated_client):
        """Test get Category detail."""

        category = example_category
        url = detail_url(category.id)
        res = authenticated_client.get(url)
        serializer = CategoryDetailSerializer(category)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == serializer.data

    def test_create_category(
            self,
            example_ecommerce_store,
            authenticated_client,
    ):
        """Test creating a Category."""

        e_store = example_ecommerce_store
        payload = {
            'parent_store': e_store.id,
            'name': 'Test Category',
            'url': 'https://test-store/test-category',
        }
        res = authenticated_client.post(CATEGORY_CREATE_URL, payload)
        category = Category.objects.first()

        assert res.status_code == status.HTTP_201_CREATED
        assert category.name == payload['name']
        assert category.url == payload['url']
        assert category.parent_store == e_store
