"""
Tests for Category related APIs
"""
import pytest
from django.urls import reverse
from rest_framework import status

from scraped.models import Category, EcommerceStore
from scraped.serializers import CategoryDetailSerializer, CategorySerializer


CATEGORY_LIST_URL = reverse('')
CATEGORY_CREATE_URL = reverse()
pytestmark = pytest.mark.django_db


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


class TestPrivateCategoryApi:
    """
    Test authenticated API requests for Category endpoints.
    """

    def test_get_categories(
            self,
            create_example_categories,
            authenticated_client,
    ):
        """"""
        pass
    