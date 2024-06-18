from django.test import Client, TestCase
from django.urls import reverse
from .models import User

class AccountsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass',
            age=30,
            phone_number='123456789',
            location='New York'
        )

    def test_user_registration(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'age': 25,
            'phone_number': '987654321',
            'location': 'London'
        }
        response = self.client.post(reverse('accounts:register'), data)
        self.assertRedirects(response, reverse('accounts:login'))
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_user_login(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertRedirects(response, reverse('blog:post_list'))
        self.assertTrue(self.client.session.get('_auth_user_id') is not None)

    def test_user_logout(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('blog:post_list'))
        self.assertTrue(self.client.session.get('_auth_user_id') is None)

    def test_user_profile_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'testuser@example.com')
        self.assertContains(response, '30')
        self.assertContains(response, '123456789')
        self.assertContains(response, 'New York')
