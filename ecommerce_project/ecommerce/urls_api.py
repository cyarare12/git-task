from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .api_views import (
    StoreListCreateView, StoreDetailView,
    ProductListCreateView, ProductDetailView,
    ReviewListCreateView, ReviewDetailView,
    vendor_stores, store_products
)

app_name = 'ecommerce_api'

@api_view(['GET'])
def api_root(request, format=None):
    """
    Root API view that lists all available endpoints.
    """
    return Response({
        'stores': reverse('ecommerce_api:store-list-create', request=request, format=format),
        'products': reverse('ecommerce_api:product-list-create', request=request, format=format),
        'reviews': reverse('ecommerce_api:review-list-create', request=request, format=format),
        'vendor-stores': reverse('ecommerce_api:vendor-stores', request=request, format=format),
    })

urlpatterns = [
    # API root
    path('', api_root, name='api-root'),

    # Store endpoints
    path('stores/', StoreListCreateView.as_view(), name='store-list-create'),
    path('stores/<int:pk>/', StoreDetailView.as_view(), name='store-detail'),

    # Product endpoints
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # Review endpoints
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),

    # Vendor specific endpoints
    path('vendor/stores/', vendor_stores, name='vendor-stores'),
    path('stores/<int:store_id>/products/', store_products, name='store-products'),
]