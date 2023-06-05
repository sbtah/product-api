from django.urls import path
from scraped import views


app_name = 'scraped'


urlpatterns = [
    path(
        'stores/',
        views.ecommerce_store_list_view,
        name="store-list",
    ),
    path(
        'stores/<int:pk>/',
        views.ecommerce_store_detail_view,
        name='store-detail',
    ),
    path(
        'stores/create/',
        views.ecommerce_store_create_view,
        name="store-create",
    ),
    path(
        'stores/<int:pk>/update/',
        views.ecommerce_store_update_view,
        name='store-update',
    ),
    path(
        'stores/<int:pk>/delete/',
        views.ecommerce_store_delete_view,
        name='store-delete',
    ),
    # TODO
    # Fix this
    # This endpoint should provide LocalStore objects for EcommerceStore.
    path(
        'stores/<int:pk>/local-stores/',
        views.ecommerce_store_local_stores_view,
        name='children-stores'
    ),
    path(
        'local-stores/',
        views.local_store_list_view,
        name='local-store-list'
    ),
    path(
        'local-stores/<int:pk>/',
        views.local_store_detail_view,
        name='local-store-detail',
    ),
    path(
        'local-stores/create/',
        views.local_store_create_view,
        name="local-store-create",
    ),
    path(
        'local-stores/<int:pk>/update/',
        views.local_store_update_view,
        name='local-store-update',
    ),
]
