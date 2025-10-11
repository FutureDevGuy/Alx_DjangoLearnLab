from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class PostCommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='p')
        self.client.login(username='u', password='p')

    def test_create_post(self):
        url = '/api/posts/'
        data = {'title':'T','content':'C'}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['title'], 'T')

    def test_create_comment(self):
        post_resp = self.client.post('/api/posts/', {'title':'T','content':'C'}, format='json')
        post_id = post_resp.data['id']
        resp = self.client.post('/api/comments/', {'post':post_id,'content':'A'}, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['content'], 'A')
