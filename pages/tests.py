from django.test import TestCase

from django.test import TestCase
from django.urls import reverse

class PortfolioTests(TestCase):

    def test_about_page_status_code(self):
        # Sostituisci 'about' con il nome che hai nel file urls.py
        response = self.client.get(reverse('pages:about'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_contains_architect_text(self):
        # Questo verifica che il tuo nuovo brand sia presente nell'HTML
        response = self.client.get(reverse('pages:about'))
        self.assertContains(response, "AI Solution Architect in training")


