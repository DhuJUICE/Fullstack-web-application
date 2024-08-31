from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIClient
from django.test import TestCase
from faq.models import FAQ
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class FaqCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_faq(self):
        data = {
            'question': 'What is your name?',
            'answer': 'My name is Test.',
        }
        response = self.client.post('/api/deserial/', data, format='json')
        self.assertEqual(response.status_code, 201)
        #self.assertEqual(FAQ.objects.count(), 1)
        #self.assertEqual(FAQ.objects.get().question, 'What is your name?')