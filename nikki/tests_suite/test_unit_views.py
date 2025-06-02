from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

class BasicViewTests(TestCase):

    @patch('nikki.views.get_anime_genres')
    @patch('nikki.views.requests.get')
    def test_homepage_loads_successfully(self, mock_get, mock_get_genres):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": [
                {
                    "mal_id": 1,
                    "title": "Test Anime",
                    "images": {"jpg": {"image_url": "https://example.com/anime.jpg"}},
                    "score": 8.7,
                    "year": 2023,
                    "type": "TV",
                    "genres": [{"name": "Action"}]
                }
            ]
        }
        mock_get_genres.return_value = [
            {"mal_id": 1, "name": "Action", "slug": "action"},
            {"mal_id": 2, "name": "Comédie", "slug": "comedie"}
        ]

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'animes/home.html')
        self.assertIn('top_animes', response.context)
        self.assertIn('anime_genres', response.context)
        self.assertGreater(len(response.context['top_animes']), 0)
        self.assertGreater(len(response.context['anime_genres']), 0)

class RobustnessTests(TestCase):

    @patch('nikki.views.get_anime_genres')
    @patch('nikki.views.requests.get')
    def test_homepage_handles_api_error(self, mock_get, mock_get_genres):
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {}
        mock_get_genres.return_value = []

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tendances actuelles")
        self.assertIn('top_animes', response.context)
        self.assertEqual(len(response.context['top_animes']), 0)

    @patch('nikki.views.get_anime_genres')
    @patch('nikki.views.requests.get')
    def test_homepage_with_incomplete_anime_data(self, mock_get, mock_get_genres):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": [
                {
                    "mal_id": 1,
                    "title": "Anime Sans Score",
                    "images": {"jpg": {"image_url": "https://example.com.jpg"}},
                    "type": "TV",
                    "year": None,
                    "genres": []
                }
            ]
        }
        mock_get_genres.return_value = []

        response = self.client.get(reverse('home'))
        self.assertContains(response, "Anime Sans Score")
        self.assertContains(response, "Genre inconnu")

    @patch('nikki.views.get_anime_genres')
    @patch('nikki.views.requests.get')
    def test_navbar_renders_even_with_empty_genres(self, mock_get, mock_get_genres):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": []}
        mock_get_genres.return_value = []

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Genres")
        self.assertContains(response, "Genres non disponibles")
