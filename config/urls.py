from django.contrib import admin
from django.urls import path
from nikki import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path("conditions-utilisation/", views.terms, name="terms"),
    path("politique-confidentialite/", views.privacy, name="privacy"),
    path("genres/<slug:slug>/", views.genre_animes, name="genre_animes"),
    path("animes/", views.animes_view, name="animes"),
    path("genres/", views.all_genres, name="all_genres"),
    path("logout/", views.logout_view, name="logout"),
    path("profil/", views.profile_view, name="profil"),
    path("login/", views.login_view, name="login"),
    path('changer-mot-de-passe/', auth_views.PasswordChangeView.as_view(template_name='users/changer_mdp.html'), name='password_change'),
    path('changer-mot-de-passe/succes/', auth_views.PasswordChangeDoneView.as_view(template_name='users/succes_mdp.html'), name='password_change_done'),
    path('supprimer-compte/', views.delete_account, name='delete_account'),
    path('supprimer-donnees/', views.delete_data, name='delete_data'),
    path('add-to-list/', views.add_anime_to_list, name='add_to_list'),
    path('ajax/change-anime-status/', views.change_anime_status_ajax, name='change_anime_status_ajax'),
    path('remove-anime/<int:user_anime_id>/', views.remove_anime, name='remove_anime'),
    path('anime/<int:anime_id>/', views.anime_detail, name='anime_detail'),
    path('toggle-episode/', views.toggle_episode_view, name='toggle_episode_view'),
]
