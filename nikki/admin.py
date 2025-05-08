from django.contrib import admin
from .models import User, Anime, UserAnime, Season, Episode, UserEpisodeView, UserSeasonView

# Register your models here.
admin.site.register(User)
admin.site.register(Anime)
admin.site.register(UserAnime)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(UserEpisodeView)
admin.site.register(UserSeasonView)