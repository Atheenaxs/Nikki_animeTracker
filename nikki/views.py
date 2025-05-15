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

def genre_animes(request, slug):
    all_genres = get_anime_genres()
    genre = next((g for g in all_genres if g['slug'] == slug), None)

    if not genre:
        return render(request, "animes/genre_not_found.html", status=404)

    mal_id = genre["mal_id"]
    response = requests.get(f"https://api.jikan.moe/v4/anime?genres={mal_id}&order_by=popularity")
    animes = response.json().get("data", [])

    return render(request, "animes/by_genre.html", {
        "genre": genre,
        "animes": animes,
        "anime_genres": all_genres,
    })

def animes_view(request):
    query = request.GET.get("q", "")
    anime_genres = get_anime_genres()

    if query:
        response = requests.get(f"https://api.jikan.moe/v4/anime?q={query}&order_by=popularity")
    else:
        response = requests.get("https://api.jikan.moe/v4/top/anime?limit=25")

    animes = response.json().get("data", [])

    return render(request, "animes/animes.html", {
        "animes": animes,
        "query": query,
        "anime_genres": anime_genres,
    })