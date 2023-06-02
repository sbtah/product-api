from rest_framework import serializers
# from rest_framework.reverse import reverse
from scraped.models import EcommerceStore, LocalStore


class EcommerceStoreSerializer(serializers.ModelSerializer):
    """Serializer for EcommerceStore."""

    class Meta:
        model = EcommerceStore
        fields = [
            'id',
            'name',
            'domain',
        ]
        read_only_fields = ['id', ]


class EcommerceStoreDetailSerializer(EcommerceStoreSerializer):
    """Detail serializer for EcommerceStore detail view."""

    class Meta(EcommerceStoreSerializer.Meta):
        fields = EcommerceStoreSerializer.Meta.fields + [
            'discovery_url',
            'package_name',
            'module_name',
            'class_name',
            'created',
            'last_scrape_start',
            'last_scrape_end',
            'is_active',
            'is_monitored',
        ]


class LocalStoreSerializer(serializers.ModelSerializer):
    """Serializer for LocalStore object."""

    class Meta:
        model = LocalStore
        fields = [
            'id',
            'name',
        ]
        read_only_fields = ['id', ]


class LocalStoreDetailSerializer(LocalStoreSerializer):
    """Detail serializer for LocalStore detail view."""

    class Meta(LocalStoreSerializer.Meta):
        fields = LocalStoreSerializer.Meta.fields + [
            'parent_store',
            'scraper_id',
            'url',
            'api_url',
            'created',
            'last_scrape_start',
            'last_scrape_end',
            'is_active',
            'is_monitored',
        ]


class EcommerceStoreLocalStoresSerializer(EcommerceStoreDetailSerializer):
    """Detail serializer for EcommerceStore used for listing all children LocalStores."""

    local_stores = LocalStoreSerializer(many=True, required=False,  read_only=True)

    class Meta(EcommerceStoreDetailSerializer.Meta):
        fields = EcommerceStoreDetailSerializer.Meta.fields + [
            'local_stores',
        ]
