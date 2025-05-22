from django.contrib import admin
from django.urls import path
from nikki import views

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
]
