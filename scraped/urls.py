from django.urls import path

from scraped.views import (
    category_views,
    ecommerce_store_views,
    local_store_views,
)


app_name = 'scraped'


urlpatterns = [
    path(
        'stores/',
        ecommerce_store_views.ecommerce_store_list_view,
        name="store-list",
    ),
    path(
        'stores/<int:pk>/',
        ecommerce_store_views.ecommerce_store_detail_view,
        name='store-detail',
    ),
    path(
        'stores/create/',
        ecommerce_store_views.ecommerce_store_create_view,
        name="store-create",
    ),
    path(
        'stores/<int:pk>/update/',
        ecommerce_store_views.ecommerce_store_update_view,
        name='store-update',
    ),
    path(
        'stores/<int:pk>/delete/',
        ecommerce_store_views.ecommerce_store_delete_view,
        name='store-delete',
    ),
    # Local Store endpoints:
    path(
        'local-stores/',
        local_store_views.local_store_list_view,
        name='local-store-list'
    ),
    path(
        'local-stores/<int:pk>/',
        local_store_views.local_store_detail_view,
        name='local-store-detail',
    ),
    path(
        'local-stores/create/',
        local_store_views.local_store_create_view,
        name="local-store-create",
    ),
    path(
        'local-stores/<int:pk>/update/',
        local_store_views.local_store_update_view,
        name='local-store-update',
    ),
    path(
        'local-stores/<int:pk>/delete/',
        local_store_views.local_store_delete_view,
        name='local-store-delete',
    ),
    # Category endpoints.
    path(
        'categories/',
        category_views.category_list_view,
        name='category-list'
    ),
    path(
        'categories/<int:pk>/',
        category_views.category_detail_view,
        name='category-detail',
    ),
]
