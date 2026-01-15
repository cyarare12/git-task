from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Publisher, Article, Newsletter, Category

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('role', 'subscribed_publishers', 'subscribed_journalists')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')

admin.site.register(Publisher)
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Newsletter)
