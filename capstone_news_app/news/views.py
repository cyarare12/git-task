from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.db import models
from django.core.mail import send_mass_mail
from django.conf import settings
import requests
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .forms import CustomUserCreationForm
from .models import Article, Newsletter, Publisher, CustomUser
from .serializers import ArticleSerializer

# Helper function to gather subscriber emails
def _gather_subscriber_emails(article):
    emails = set()
    if article.publisher:
        emails.update(article.publisher.subscribers.values_list('email', flat=True))
    # subscribers to article author (journalist)
    emails.update(article.author.subscriber_of.values_list('email', flat=True))
    return [e for e in emails if e]

class CustomLoginView(LoginView):
    template_name = 'news/login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('article_list')

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'news/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('article_list')

class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 9  # 9 articles per page (3x3 grid)

    def get_queryset(self):
        queryset = Article.objects.filter(approved=True).order_by('-published_at')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                models.Q(title__icontains=query) |
                models.Q(body__icontains=query) |
                models.Q(author__username__icontains=query) |
                models.Q(publisher__name__icontains=query)
            )
        return queryset

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    template_name = 'news/article_form.html'
    fields = ['title', 'body', 'image', 'publisher', 'categories']
    permission_required = 'news.add_article'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class NewsletterCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Newsletter
    template_name = 'news/newsletter_form.html'
    fields = ['title', 'content', 'publisher']
    permission_required = 'news.add_newsletter'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    template_name = 'news/newsletter_list.html'
    context_object_name = 'newsletters'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'reader':
            # Newsletters from subscribed publishers and journalists
            publishers = user.subscribed_publishers.all()
            journalists = user.subscribed_journalists.all()
            return Newsletter.objects.filter(
                models.Q(publisher__in=publishers) | models.Q(author__in=journalists)
            )
        elif user.role == 'journalist':
            # Newsletters by the user
            return Newsletter.objects.filter(author=user)
        return Newsletter.objects.none()


def is_editor(user):
    return getattr(user, 'role', '') == 'editor' or user.groups.filter(name='Editor').exists()

@login_required
@user_passes_test(is_editor)
def pending_articles(request):
    articles = Article.objects.filter(approved=False).order_by('-created_at')
    return render(request, 'news/pending_list.html', {'articles': articles})

@login_required
@user_passes_test(is_editor)
def approve_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.approve()

    # Send email to subscribers
    emails = _gather_subscriber_emails(article)
    if emails:
        subject = f"New article published: {article.title}"
        message = article.body[:500] + "\n\nRead more on the site."
        from_email = settings.DEFAULT_FROM_EMAIL
        datatuple = [(subject, message, from_email, [email]) for email in emails]
        send_mass_mail(datatuple, fail_silently=True)

    # Post to X (Twitter) via HTTP API
    try:
        x_api_url = getattr(settings, 'X_API_POST_URL', None)
        x_bearer = getattr(settings, 'X_API_BEARER', None)
        if x_api_url and x_bearer:
            headers = {"Authorization": f"Bearer {x_bearer}", "Content-Type": "application/json"}
            payload = {"text": f"{article.title}\n{article.body[:240]}"}
            requests.post(x_api_url, json=payload, headers=headers, timeout=5)
    except Exception:
        # intentionally silent; production should log
        pass

    return redirect('news:pending_articles')
