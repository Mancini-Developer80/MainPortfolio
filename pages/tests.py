from django.test import TestCase
from django.urls import reverse

class PortfolioTests(TestCase):

    def test_about_page_status_code(self):
        # Usiamo follow=True per gestire eventuali redirect 301/302 automatici
        response = self.client.get(reverse('pages:about'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_about_page_contains_architect_text(self):
        # Verifica che il brand sia presente dopo aver seguito eventuali redirect
        response = self.client.get(reverse('pages:about'), follow=True)
        self.assertContains(response, "AI Solution Architect")