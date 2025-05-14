import requests
from django.shortcuts import render
from nikki.utils import get_anime_genres

def home(request):
    response = requests.get("https://api.jikan.moe/v4/top/anime")
    top_animes = []

    if response.status_code == 200:
        data = response.json()
        top_animes = data.get("data", [])[:10]  # on prend les 10 premiers

    anime_genres = get_anime_genres()
    return render(request, "animes/home.html", {
        "top_animes": top_animes,
        "anime_genres": anime_genres,
    })

def terms(request):
    return render(request, "legal/terms.html")

def privacy(request):
    return render(request, "legal/privacy.html")

def genre_animes(request, mal_id):
    animes = requests.get(f"https://api.jikan.moe/v4/anime?genres={mal_id}&order_by=popularity").json().get("data", [])
    anime_genres = get_anime_genres()
    return render(request, "animes/by_genre.html", {
        "animes": animes,
        "anime_genres": anime_genres,
    })