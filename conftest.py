'''
Fixtures
'''
import pytest
from scraped import models


@pytest.fixture
def example_ecommerce_store():
    '''Pytest fixture for creating example EcommerceStore object.'''
    return models.EcommerceStore.objects.create(
        name='Test Store',
        domain='test-store.com',
        discovery_url='https://test-store.com/',
    )


@pytest.fixture
def example_local_store(example_ecommerce_store):
    '''Pytest fixture for creating example LocalSore object.'''
    e_store = example_ecommerce_store
    return models.LocalStore.objects.create(
        parrent_store=e_store,
        name='New York',
        scraped_id=1,
        is_active=True,
    )

@pytest.fixture
def example_category(example_ecommerce_store):
    '''Pytest fixture for creating example Category object.'''
    e_store = example_ecommerce_store
    return models.Category.objects.create(
        parrent_store=e_store,
        name='Test Category',
        url = 'https://test-store/test-category'
    )

@pytest.fixture
def example_product(example_ecommerce_store):
    '''Pytest fixture for creating example Product object.'''
    e_store = example_ecommerce_store
    return models.Product.objects.create(
        parrent_store=e_store,
        name='Test Product',
        url = 'https://test-store/test-product'
    )