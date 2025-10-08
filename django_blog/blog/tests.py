from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post

class TagSearchTests(TestCase):
    def setUp(self):
        u = User.objects.create_user('bob', password='pw')
        p1 = Post.objects.create(title='Django tips', content='content', author=u)
        p1.tags.add('django', 'tips')
        p2 = Post.objects.create(title='Flask stuff', content='flask content', author=u)
        p2.tags.add('flask')

    def test_search_title(self):
        resp = self.client.get('/search/?q=django')
        self.assertContains(resp, 'Django tips')

    def test_search_tag(self):
        resp = self.client.get('/search/?q=tips')
        self.assertContains(resp, 'Django tips')

    def test_posts_by_tag(self):
        resp = self.client.get('/tags/django/')
        self.assertContains(resp, 'Django tips')
        self.assertNotContains(resp, 'Flask stuff')
