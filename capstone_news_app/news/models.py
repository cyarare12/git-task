from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # publisher can have many editors and journalists (via User.groups or explicit M2M)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    ROLE_READER = 'reader'
    ROLE_JOURNALIST = 'journalist'
    ROLE_EDITOR = 'editor'
    ROLE_CHOICES = (
        (ROLE_READER, 'Reader'),
        (ROLE_JOURNALIST, 'Journalist'),
        (ROLE_EDITOR, 'Editor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_READER)
    # Reader fields
    subscribed_publishers = models.ManyToManyField(Publisher, blank=True, related_name='subscribers')
    subscribed_journalists = models.ManyToManyField(
        'self', blank=True, symmetrical=False, related_name='subscriber_of'
    )
    # Journalist fields are represented via related_name on Article and Newsletter models

    def save(self, *args, **kwargs):
        """
        Enforce mutual exclusivity: if journalist, clear reader subscription fields;
        if reader, clear journalist-specific relationships (none to clear here except role-based checks).
        """
        is_new = self.pk is None
        if self.role == self.ROLE_JOURNALIST:
            # journalists shouldn't have reader subscriptions
            super().save(*args, **kwargs)
            self.subscribed_publishers.clear()
            self.subscribed_journalists.clear()
        else:
            super().save(*args, **kwargs)
        # Assign to group
        if self.role:
            group_name = self.role.capitalize()
            try:
                group = Group.objects.get(name=group_name)
                if is_new or not self.groups.filter(name=group_name).exists():
                    self.groups.add(group)
            except Group.DoesNotExist:
                pass  # groups not created yet

class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True, help_text="Upload an image that represents the article")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    publisher = models.ForeignKey(Publisher, null=True, blank=True, on_delete=models.SET_NULL, related_name='articles')
    categories = models.ManyToManyField(Category, blank=True, related_name='articles')
    approved = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def approve(self):
        self.approved = True
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Newsletter(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='newsletters')
    publisher = models.ForeignKey(Publisher, null=True, blank=True, on_delete=models.SET_NULL, related_name='newsletters')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
