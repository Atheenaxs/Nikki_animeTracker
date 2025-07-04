from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    email = models.EmailField(unique=True)
    watch_time = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.email


class Anime(models.Model):
    mal_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    synopsis = models.TextField(blank=True)
    synopsis_fr = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=50)
    release_date = models.DateField(blank=True, null=True)
    nb_episodes = models.PositiveIntegerField(default=1)

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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    rating = models.IntegerField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'anime')

    def __str__(self):
        return f"{self.user.username} - {self.anime.title} ({self.status})"


class Episode(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    episode_number = models.IntegerField()
    title = models.CharField(max_length=255)
    title_fr = models.CharField(max_length=255, blank=True, null=True)
    air_date = models.DateField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('anime', 'episode_number')

    def __str__(self):
        return f"{self.anime.title} - Épisode {self.episode_number}"


class UserEpisodeView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    is_watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'episode')

    def __str__(self):
        return f"{self.user.username} - {self.episode} - Vu : {self.is_watched}"

