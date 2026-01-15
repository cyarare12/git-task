from rest_framework import serializers
from .models import Store, Product, Review, Profile

class ProfileSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['user_username', 'user_email', 'role']

class StoreSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'name', 'description', 'owner', 'owner_username', 'products_count']
        read_only_fields = ['owner']

    def get_products_count(self, obj):
        return obj.product_set.count()

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class ProductSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'store', 'store_name', 'reviews_count', 'average_rating']
        read_only_fields = ['store']

    def get_reviews_count(self, obj):
        return obj.review_set.count()

    def get_average_rating(self, obj):
        reviews = obj.review_set.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    def create(self, validated_data):
        store_id = self.context['request'].data.get('store')
        if store_id:
            store = Store.objects.get(id=store_id, owner=self.context['request'].user)
            validated_data['store'] = store
        return super().create(validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_username', 'product', 'product_name', 'rating', 'comment', 'verified', 'created_at']
        read_only_fields = ['user', 'verified']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        product = validated_data['product']
        # Check if user has purchased this product
        from .models import OrderItem
        validated_data['verified'] = OrderItem.objects.filter(
            order__user=self.context['request'].user,
            product=product
        ).exists()
        return super().create(validated_data)