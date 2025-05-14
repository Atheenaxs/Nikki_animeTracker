from django.contrib import admin
from django.urls import path
from nikki import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path("conditions-utilisation/", views.terms, name="terms"),
    path("politique-confidentialite/", views.privacy, name="privacy"),
    path("genres/<slug:slug>/", views.genre_animes, name="genre_animes"),
]
