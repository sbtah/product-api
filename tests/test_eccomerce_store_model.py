'''
Tests for EcommerceStore model.
'''
import pytest
from objects.models import stores


pytestmark = pytest.mark.django_db


class TestEcommerceStoreModel:
    '''Test cases related to EcommerceStore objects.'''

    def test_create_ecommerce_store(self):
        '''Test creating EcommerceStore object is sucessful.'''

        assert stores.EcommerceStore.objects.all().count() == 0
        e_store = stores.EcommerceStore.objects.create(
            name="Test Store",
            domain="test-store.com",
            discovery_url='https://test-store.com/',
        )
        assert stores.EcommerceStore.objects.all().count() == 1
        assert isinstance(e_store, stores.EcommerceStore) is True

    def test_ecommerce_store_str_method(self, example_ecommerce_store):
        '''Test that __str__ for EcommerceStore is properly generated.'''

        e_store = example_ecommerce_store
        assert str(e_store) == e_store.name

    def test_save_method_sets_created_field(self, example_ecommerce_store):
        '''Test save method on class.'''

        e_store = example_ecommerce_store

        assert e_store.created is not None
        assert isinstance(e_store.created, int)
        assert issubclass(stores.EcommerceStore, stores.ScrapedObject)
