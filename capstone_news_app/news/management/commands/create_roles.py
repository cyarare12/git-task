from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

class Command(BaseCommand):
    help = 'Create Reader, Journalist, Editor groups with permissions'

    def handle(self, *args, **options):
        Article = apps.get_model('news', 'Article')
        Newsletter = apps.get_model('news', 'Newsletter')
        # perms
        view_article = Permission.objects.get(codename='view_article')
        add_article = Permission.objects.get(codename='add_article')
        change_article = Permission.objects.get(codename='change_article')
        delete_article = Permission.objects.get(codename='delete_article')
        view_news = Permission.objects.get(codename='view_newsletter')
        add_news = Permission.objects.get(codename='add_newsletter')
        change_news = Permission.objects.get(codename='change_newsletter')
        delete_news = Permission.objects.get(codename='delete_newsletter')
        reader, _ = Group.objects.get_or_create(name='Reader')
        reader.permissions.set([view_article, view_news])
        journalist, _ = Group.objects.get_or_create(name='Journalist')
        journalist.permissions.set([view_article, add_article, change_article, delete_article,
                                    view_news, add_news, change_news, delete_news])
        editor, _ = Group.objects.get_or_create(name='Editor')
        editor.permissions.set([view_article, change_article, delete_article,
                                view_news, change_news, delete_news])
        self.stdout.write('Groups created/updated.')