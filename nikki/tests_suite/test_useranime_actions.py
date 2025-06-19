from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
import json

from nikki.models import Anime, Episode, UserAnime, UserEpisodeView

User = get_user_model()

# Fonction utilitaire pour créer des épisodes fictifs liés à un anime
def create_stub_episodes(anime, count=2):
    for num in range(1, count + 1):
        Episode.objects.create(
            anime=anime,
            episode_number=num,
            title=f"Ep {num}"
        )
    anime.nb_episodes = count
    anime.save()

# Tests des actions utilisateur liées à la gestion des animes
class UserAnimeActionsTests(TestCase):

    # Setup : création d'un utilisateur de test connecté
    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test@example.com", password="pass"
        )
        self.client.login(email="test@example.com", password="pass")

    # Test : ajout d'un anime à la liste (avec création simulée des épisodes)
    @patch("nikki.views.create_episodes")
    def test_add_anime_to_list(self, mock_create):
        def fake_create(anime):
            create_stub_episodes(anime, 2)
        mock_create.side_effect = fake_create

        payload = {
            "anime_id": 123,
            "status": "watching",
            "title": "My Anime",
            "image_url": "http://img"
        }
        response = self.client.post(
            reverse("add_to_list"),
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # Vérifie que l'anime a bien été ajouté à la liste
        ua = UserAnime.objects.get(user=self.user, anime__mal_id=123)
        self.assertEqual(ua.status, "watching")
        self.assertEqual(ua.anime.nb_episodes, 2)

    # Méthode utilitaire interne : crée un anime et des épisodes associés
    def _setup_anime_with_views(self):
        anime = Anime.objects.create(mal_id=1, title="Anime", nb_episodes=2)
        for i in range(1, 3):
            Episode.objects.create(anime=anime, episode_number=i, title=f"Ep {i}")
        ua = UserAnime.objects.create(user=self.user, anime=anime, status="watching")
        return anime, ua

    # Test : marquer un épisode comme vu
    def test_mark_episode_as_watched(self):
        anime, ua = self._setup_anime_with_views()
        ep = anime.episode_set.first()
        payload = {"episode_id": ep.id, "watched": True}
        response = self.client.post(
            reverse("toggle_episode_view"),
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        ev = UserEpisodeView.objects.get(user=self.user, episode=ep)
        self.assertTrue(ev.is_watched)

        # Le statut doit rester "watching"
        ua.refresh_from_db()
        self.assertEqual(ua.status, "watching")

    # Test : si tous les épisodes sont vus, le statut passe à "finished"
    def test_auto_finished_when_all_watched(self):
        anime, ua = self._setup_anime_with_views()
        episodes = list(anime.episode_set.all())
        for ep in episodes:
            payload = {"episode_id": ep.id, "watched": True}
            self.client.post(
                reverse("toggle_episode_view"),
                data=json.dumps(payload),
                content_type="application/json",
            )
        ua.refresh_from_db()
        self.assertEqual(ua.status, "finished")

    # Test : suppression d’un anime -> doit aussi supprimer les épisodes vus
    def test_remove_anime_deletes_entries(self):
        anime, ua = self._setup_anime_with_views()
        for ep in anime.episode_set.all():
            UserEpisodeView.objects.create(user=self.user, episode=ep, is_watched=True)
        response = self.client.post(reverse("remove_anime", args=[ua.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(UserAnime.objects.filter(id=ua.id).exists())
        self.assertEqual(
            UserEpisodeView.objects.filter(user=self.user, episode__anime=anime).count(),
            0,
        )

    # Test : si un anime est ajouté avec le statut "finished", tous les épisodes sont marqués vus automatiquement
    @patch("nikki.views.create_episodes")
    def test_add_finished_marks_episodes_watched(self, mock_create):
        def fake_create(anime):
            create_stub_episodes(anime, 2)
        mock_create.side_effect = fake_create

        payload = {
            "anime_id": 456,
            "status": "finished",
            "title": "Completed Anime",
            "image_url": "http://img"
        }
        self.client.post(
            reverse("add_to_list"),
            data=json.dumps(payload),
            content_type="application/json",
        )
        anime = Anime.objects.get(mal_id=456)
        views = UserEpisodeView.objects.filter(user=self.user, episode__anime=anime)

        self.assertEqual(views.count(), 2)
        self.assertTrue(all(v.is_watched for v in views))
