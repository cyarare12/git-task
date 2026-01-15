from django.urls import reverse
from rest_framework.test import APITestCase
from .models import CustomUser, Article, Publisher

class ArticleAPITest(APITestCase):
    def setUp(self):
        self.journalist = CustomUser.objects.create_user(username='j1', password='pass', role='journalist', email='j1@example.com')
        self.reader = CustomUser.objects.create_user(username='r1', password='pass', role='reader', email='r1@example.com')
        self.publisher = Publisher.objects.create(name='Pub1')
        self.article1 = Article.objects.create(title='T1', body='B', author=self.journalist, publisher=self.publisher, approved=True)
        self.article2 = Article.objects.create(title='T2', body='B2', author=self.journalist, approved=True)
        # Subscribe reader to publisher and journalist
        self.reader.subscribed_publishers.add(self.publisher)
        self.reader.subscribed_journalists.add(self.journalist)

    def test_get_articles_authenticated(self):
        self.client.force_authenticate(user=self.reader)
        url = reverse('api_articles')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 2)  # both articles
        titles = [a['title'] for a in data]
        self.assertIn('T1', titles)
        self.assertIn('T2', titles)

    def test_get_articles_unauthenticated(self):
        url = reverse('api_articles')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

    def test_get_articles_no_subscriptions(self):
        reader2 = CustomUser.objects.create_user(username='r2', password='pass', role='reader', email='r2@example.com')
        self.client.force_authenticate(user=reader2)
        url = reverse('api_articles')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 0)

    def test_get_publisher_articles_subscribed(self):
        self.client.force_authenticate(user=self.reader)
        url = reverse('api_publisher_articles', kwargs={'publisher_id': self.publisher.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'T1')

    def test_get_publisher_articles_not_subscribed(self):
        reader2 = CustomUser.objects.create_user(username='r2', password='pass', role='reader', email='r2@example.com')
        self.client.force_authenticate(user=reader2)
        url = reverse('api_publisher_articles', kwargs={'publisher_id': self.publisher.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

    def test_get_journalist_articles_subscribed(self):
        self.client.force_authenticate(user=self.reader)
        url = reverse('api_journalist_articles', kwargs={'journalist_id': self.journalist.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 2)  # both articles by journalist
        titles = [a['title'] for a in data]
        self.assertIn('T1', titles)
        self.assertIn('T2', titles)

    def test_get_journalist_articles_not_subscribed(self):
        reader2 = CustomUser.objects.create_user(username='r2', password='pass', role='reader', email='r2@example.com')
        self.client.force_authenticate(user=reader2)
        url = reverse('api_journalist_articles', kwargs={'journalist_id': self.journalist.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)
