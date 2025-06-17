from django.contrib import admin
from .models import User, Anime, UserAnime, Episode, UserEpisodeView

# Register your models here.
admin.site.register(User)
admin.site.register(Anime)
admin.site.register(UserAnime)
admin.site.register(Episode)
admin.site.register(UserEpisodeView)