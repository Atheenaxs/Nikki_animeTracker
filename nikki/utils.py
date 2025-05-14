import requests
from django.utils.text import slugify

def get_anime_genres():
    response = requests.get("https://api.jikan.moe/v4/genres/anime")
    genres = response.json().get("data", [])

    for genre in genres:
        genre["slug"] = slugify(genre["name"])

    # 🔠 Tri alphabétique par nom
    genres.sort(key=lambda g: g["name"].lower())

    return genres
