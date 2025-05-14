import requests
from django.shortcuts import render

def home(request):
    response = requests.get("https://api.jikan.moe/v4/top/anime")
    top_animes = []

    if response.status_code == 200:
        data = response.json()
        top_animes = data.get("data", [])[:10]  # on prend les 10 premiers

    return render(request, "animes/home.html", {"top_animes": top_animes})

def terms(request):
    return render(request, "legal/terms.html")

def privacy(request):
    return render(request, "legal/privacy.html")