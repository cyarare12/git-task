from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Store, Product, Review
from .serializers import StoreSerializer, ProductSerializer, ReviewSerializer

# Store API Views
class StoreListCreateView(generics.ListCreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.profile.role == 'vendor':
            return Store.objects.filter(owner=self.request.user)
        return Store.objects.all()

    def perform_create(self, serializer):
        if self.request.user.profile.role != 'vendor':
            raise permissions.PermissionDenied("Only vendors can create stores")
        serializer.save()

class StoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.profile.role == 'vendor':
            return Store.objects.filter(owner=self.request.user)
        return Store.objects.all()

# Product API Views
class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.all()
        store_id = self.request.query_params.get('store', None)
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        return queryset

    def perform_create(self, serializer):
        if self.request.user.profile.role != 'vendor':
            raise permissions.PermissionDenied("Only vendors can create products")
        serializer.save()

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()

    def perform_update(self, serializer):
        product = self.get_object()
        if product.store.owner != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own products")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.store.owner != self.request.user:
            raise permissions.PermissionDenied("You can only delete your own products")
        instance.delete()

# Review API Views
class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Review.objects.all()
        product_id = self.request.query_params.get('product', None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save()

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()

    def perform_update(self, serializer):
        review = self.get_object()
        if review.user != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own reviews")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise permissions.PermissionDenied("You can only delete your own reviews")
        instance.delete()

# Vendor's stores and products
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def vendor_stores(request):
    if request.user.profile.role != 'vendor':
        return Response({"error": "Only vendors can access this endpoint"}, status=status.HTTP_403_FORBIDDEN)

    stores = Store.objects.filter(owner=request.user)
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def store_products(request, store_id):
    try:
        store = Store.objects.get(id=store_id)
        # Allow access if user is vendor who owns the store or any buyer
        if request.user.profile.role == 'vendor' and store.owner != request.user:
            return Response({"error": "You can only view your own store products"}, status=status.HTTP_403_FORBIDDEN)

        products = Product.objects.filter(store=store)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Store.DoesNotExist:
        return Response({"error": "Store not found"}, status=status.HTTP_404_NOT_FOUND)