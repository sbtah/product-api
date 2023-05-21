'''
Fixtures
'''
import pytest
from objects.models import stores


@pytest.fixture
def example_ecommerce_store():
    '''Pytest fixture for creating example EcommerceStore object.'''
    return stores.EcommerceStore.objects.create(
        name='Test Store',
        domain='test-store.com',
        discovery_url='https://test-store.com/',
    )


@pytest.fixture
def example_local_store(example_ecommerce_store):
    '''Pytest fixture for creating example LocalSore object.'''
    e_store = example_ecommerce_store
    return stores.LocalStore.objects.create(
        parrent_store=e_store,
        name='New York',
        scraped_id=1,
        is_active=True,
    )
