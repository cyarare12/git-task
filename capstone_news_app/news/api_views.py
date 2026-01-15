from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Article, Publisher, CustomUser
from .serializers import ArticleSerializer

class ArticleListAPI(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Get articles from subscribed publishers and journalists
        subscribed_publishers = user.subscribed_publishers.all()
        subscribed_journalists = user.subscribed_journalists.all()
        qs = Article.objects.filter(approved=True).order_by('-published_at')
        qs = qs.filter(
            models.Q(publisher__in=subscribed_publishers) | models.Q(author__in=subscribed_journalists)
        )
        return qs

class PublisherArticlesAPI(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        publisher_id = self.kwargs['publisher_id']
        publisher = get_object_or_404(Publisher, pk=publisher_id)
        # Check if user is subscribed to this publisher
        if not user.subscribed_publishers.filter(pk=publisher_id).exists():
            raise PermissionDenied("You are not subscribed to this publisher.")
        return Article.objects.filter(publisher=publisher, approved=True).order_by('-published_at')

class JournalistArticlesAPI(ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        journalist_id = self.kwargs['journalist_id']
        journalist = get_object_or_404(CustomUser, pk=journalist_id, role='journalist')
        # Check if user is subscribed to this journalist
        if not user.subscribed_journalists.filter(pk=journalist_id).exists():
            raise PermissionDenied("You are not subscribed to this journalist.")
        return Article.objects.filter(author=journalist, approved=True).order_by('-published_at')