from django.urls import path
from .api_views import ArticleListAPI, PublisherArticlesAPI, JournalistArticlesAPI

urlpatterns = [
    path('articles/', ArticleListAPI.as_view(), name='api_articles'),
    path('publishers/<int:publisher_id>/articles/', PublisherArticlesAPI.as_view(), name='api_publisher_articles'),
    path('journalists/<int:journalist_id>/articles/', JournalistArticlesAPI.as_view(), name='api_journalist_articles'),
]