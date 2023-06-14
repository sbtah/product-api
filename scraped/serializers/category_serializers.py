from rest_framework import serializers
from scraped.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category object."""

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'parent_store',
            'scraped_id',
        ]
        read_only_fields = ['id', ]


class CategoryDetailSerializer(CategorySerializer):
    """Detail serializer for Category detail view."""

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + [
            'url',
            'api_url',
            'has_children',
            'has_products',
            'category_level',
            'parent_category_id',
            'product_count',
            'children_category_count',
            'created',
            'last_scrape_start',
            'last_scrape_end',
            'is_active',
            'is_monitored',
        ]
