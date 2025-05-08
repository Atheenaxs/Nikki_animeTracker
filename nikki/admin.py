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

#custom
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'release_date', 'image_preview')  # Affiche l'image et d'autres champs
    search_fields = ['title']  # Recherche par titre
    list_filter = ['status']  # Filtre par statut (en cours, terminé)
    
    # Ajouter une méthode pour afficher un aperçu de l'image
    def image_preview(self, obj):
        return f'<img src="{obj.image_url}" width="50" height="50" />'
    image_preview.allow_tags = True  # Permet d'afficher les images HTML dans l'admin

admin.site.register(Anime, AnimeAdmin)

class UserAnimeAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'status', 'rating', 'added_at')  # Affiche l'utilisateur, l'anime, le statut, la note et la date d'ajout
    search_fields = ['user__username', 'anime__title']  # Recherche par nom d'utilisateur ou titre de l'anime
    list_filter = ['status']  # Filtre par statut (To Watch, Watching, Finished)
    ordering = ['added_at']  # Trie par date d'ajout (de la plus récente à la plus ancienne)

admin.site.register(UserAnime, UserAnimeAdmin)

class SeasonAdmin(admin.ModelAdmin):
    list_display = ('anime', 'season_number', 'title')  # Affiche l'anime, le numéro de saison et le titre
    search_fields = ['anime__title']  # Recherche par titre d'anime
    list_filter = ['anime']  # Filtre par anime (afficher les saisons d'un anime particulier)

admin.site.register(Season, SeasonAdmin)

class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('season', 'episode_number', 'title', 'air_date')  # Affiche la saison, le numéro d'épisode, le titre et la date de diffusion
    search_fields = ['season__anime__title', 'title']  # Recherche par titre d'anime ou titre d'épisode
    list_filter = ['season']  # Filtrer les épisodes par saison

admin.site.register(Episode, EpisodeAdmin)

class UserEpisodeViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'episode', 'is_watched')  # Affiche l'utilisateur, l'épisode et l'état de vue
    search_fields = ['user__username', 'episode__title']  # Recherche par nom d'utilisateur ou titre d'épisode
    list_filter = ['user']  # Filtrer par utilisateur

admin.site.register(UserEpisodeView, UserEpisodeViewAdmin)

class UserSeasonViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'season', 'is_watched')  # Affiche l'utilisateur, la saison et l'état de vue
    search_fields = ['user__username', 'season__anime__title']  # Recherche par nom d'utilisateur ou titre d'anime
    list_filter = ['user']  # Filtrer par utilisateur

admin.site.register(UserSeasonView, UserSeasonViewAdmin)
