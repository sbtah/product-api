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
