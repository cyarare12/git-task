from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register(r'articles', views.ArticleListAPI, basename='article-api')

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('pending/', views.pending_articles, name='pending_articles'),
    path('approve/<int:pk>/', views.approve_article, name='approve_article'),
    path('newsletters/', views.NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletter/create/', views.NewsletterCreateView.as_view(), name='newsletter_create'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('api/', include('news.urls_api')),
]