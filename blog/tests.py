from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post, Comment
from django.utils import timezone

User = get_user_model()


class BlogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', is_staff=True)
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user,
            created_date=timezone.now()
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a test comment.',
            is_approved=True
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:post_detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'This is a test comment.')

    def test_create_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'New Post',
            'content': 'This is a new post.',
            'author': self.user.id,
            'created_date': '2023-06-18 12:00:00',
        })
        self.assertRedirects(response, reverse('blog:post_list'))
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_update_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('blog:post_update', args=[self.post.id]), {
            'title': 'Updated Post',
            'content': 'This is an updated post.',
        })
        self.assertRedirects(response, reverse('blog:post_list'))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')
        self.assertEqual(self.post.content, 'This is an updated post.')

    def test_delete_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('blog:post_delete', args=[self.post.id]))
        self.assertRedirects(response, reverse('blog:post_list'))
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())
