"""
Fixtures
"""
import pytest
from scraped import models
from django.contrib.auth import get_user_model


@pytest.fixture
def example_superuser_payload():
    """Dictionary of data used for creating example standard user object."""
    return {
        'email': 'admin@example.com',
        'full_name': 'Admin Admin',
        'password': 'testpass123!',
    }


@pytest.fixture
def example_superuser(example_superuser_payload):
    """Pytest fixture for creating example superuser user object."""
    data = example_superuser_payload
    return get_user_model().objects.create_superuser(
        email=data['email'],
        full_name=data['full_name'],
        password=data['password'],
    )


@pytest.fixture
def example_user_payload():
    """Dictionary of data used for creating example standard user object."""
    return {
        'email': 'user@example.com',
        'full_name': 'Joe Doe',
        'password': 'testpass321!',
    }


@pytest.fixture
def example_user(example_user_payload):
    """Pytest fixture for creating example standard user object."""
    data = example_user_payload
    return get_user_model().objects.create_user(
        email=data['email'],
        full_name=data['full_name'],
        password=data['password'],
    )


@pytest.fixture
def example_ecommerce_store():
    """Pytest fixture for creating example EcommerceStore object."""
    return models.EcommerceStore.objects.create(
        name='Test Store',
        domain='test-store.com',
        discovery_url='https://test-store.com/',
    )


@pytest.fixture
def example_ecommerce_store_2():
    """Pytest fixture for creating second example EcommerceStore object."""
    return models.EcommerceStore.objects.create(
        name='Test Store 2',
        domain='test-store-two.com',
        discovery_url='https://test-store-two.com/',
    )


@pytest.fixture
def example_local_store(example_ecommerce_store):
    """Pytest fixture for creating example LocalSore object."""
    e_store = example_ecommerce_store
    return models.LocalStore.objects.create(
        parent_store=e_store,
        name='New York',
        scraped_id=1,
        is_active=True,
    )


@pytest.fixture
def create_example_local_stores(example_ecommerce_store):
    """Create and return list of LocalStore objects."""
    e_store = example_ecommerce_store
    return [
        models.LocalStore.objects.create(
            parent_store=e_store,
            name=f'Local Store nr:{_}',
            scraped_id=_,
            is_active=True,
        )
        for _ in range(1, 4)
    ]


@pytest.fixture
def example_category(example_ecommerce_store):
    """Pytest fixture for creating example Category object."""
    e_store = example_ecommerce_store
    return models.Category.objects.create(
        parent_store=e_store,
        name='Test Category',
        url='https://test-store/test-category'
    )


@pytest.fixture
def create_example_categories(example_ecommerce_store):
    """Create and return list of Category objects."""
    e_store = example_ecommerce_store
    return [
        models.Category.objects.create(
            parent_store=e_store,
            name=f'Test Category {_}',
            url=f'https://test_category-{_}.com/',
            scraped_id=_,
        )
        for _ in range(1, 4)
    ]


@pytest.fixture
def example_product(example_ecommerce_store):
    """Pytest fixture for creating example Product object."""
    e_store = example_ecommerce_store
    return models.Product.objects.create(
        parent_store=e_store,
        name='Test Product',
        url = 'https://test-store/test-product'
    )


# Views related fixtures
@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authenticated_client(example_user, api_client):
    user = example_user
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
