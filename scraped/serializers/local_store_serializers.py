from rest_framework import serializers
from scraped.models import LocalStore


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
            'scraped_id',
            'url',
            'api_url',
            'created',
            'last_scrape_start',
            'last_scrape_end',
            'is_active',
            'is_monitored',
        ]
