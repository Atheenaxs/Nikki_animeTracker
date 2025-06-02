from django.test import TestCase
from django.urls import reverse

class HomeIntegrationTests(TestCase):

    def test_navbar_links_present(self):
        response = self.client.get(reverse('home'))
        for label in ['Accueil', 'Animes', 'Genres']:
            self.assertContains(response, label)

    def test_login_and_signup_buttons_visible(self):
        response = self.client.get(reverse('home'))
        for label in ['Connexion', 'Inscription']:
            self.assertContains(response, label)

    def test_cta_section_present(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Prêt à commencer votre aventure ?')

    def test_footer_links_present(self):
        response = self.client.get(reverse('home'))
        for label in ["Conditions d'utilisation", "Politique de confidentialité", "FAQ"]:
            self.assertContains(response, label)
