from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    avatar = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username


class Anime(models.Model):
    title = models.CharField(max_length=255)
    synopsis = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=50)
    release_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title


class UserAnime(models.Model):
    STATUS_CHOICES = [
        ('toWatch', 'To Watch'),
        ('watching', 'Watching'),
        ('finished', 'Finished'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    rating = models.IntegerField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'anime')

    def __str__(self):
        return f"{self.user.username} - {self.anime.title} ({self.status})"


class Season(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    season_number = models.IntegerField()
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('anime', 'season_number')

    def __str__(self):
        return f"{self.anime.title} - Season {self.season_number}"


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    episode_number = models.IntegerField()
    title = models.CharField(max_length=255)
    air_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('season', 'episode_number')

    def __str__(self):
        return f"{self.season} - Ep {self.episode_number}"


class UserEpisodeView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    is_watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'episode')

    def __str__(self):
        return f"{self.user.username} - {self.episode} - Watched: {self.is_watched}"


class UserSeasonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    is_watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'season')

    def __str__(self):
        return f"{self.user.username} - {self.season} - Watched: {self.is_watched}"
