from rest_framework import serializers
from .models import Article, Newsletter

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    publisher = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'body', 'author', 'publisher', 'published_at')

class NewsletterSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    publisher = serializers.StringRelatedField()

    class Meta:
        model = Newsletter
        fields = ['id', 'title', 'content', 'author', 'publisher', 'created_at']