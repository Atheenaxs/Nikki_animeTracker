from django.test import TestCase
from django.urls import reverse
# Create your tests here.

class BasicViewTests(TestCase):
    def test_homepage_loads_successfully(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)