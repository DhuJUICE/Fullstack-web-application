from django.test import TestCase
from .models import FAQ

class FAQModelTest(TestCase):

    def setUp(self):
        # Create an instance of FAQ for testing
        self.faq = FAQ.objects.create(question='What is Django?', answer='Django is a web framework.')

    def test_faq_creation(self):
        # Test that the FAQ instance was created successfully
        self.assertEqual(self.faq.question, 'What is Django?')
        self.assertEqual(self.faq.answer, 'Django is a web framework.')

    def test_faq_str(self):
        # Test the string representation of the FAQ model
        self.assertEqual(str(self.faq), 'What is Django?')  # Assuming you want to represent it by question