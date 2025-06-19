import requests
from django.utils.text import slugify
from datetime import datetime
from .models import Anime, Episode, UserEpisodeView
from django.http import HttpResponseNotFound
from deep_translator import GoogleTranslator, exceptions

def safe_translate(text, target='fr'):
    try:
        if text and isinstance(text, str) and len(text) <= 5000:
            return GoogleTranslator(source='auto', target=target).translate(text)
    except exceptions.NotValidPayload:
        pass
    return text

def get_anime_genres():
    response = requests.get("https://api.jikan.moe/v4/genres/anime")
    genres = response.json().get("data", [])

    for genre in genres:
        genre["slug"] = slugify(genre["name"])
    genres.sort(key=lambda g: g["name"].lower())
    return genres

def get_or_create_anime_or_404(request, mal_id):
    try:
        return Anime.objects.get(mal_id=mal_id)
    except Anime.DoesNotExist:
        response = requests.get(f"https://api.jikan.moe/v4/anime/{mal_id}")
        if response.status_code != 200:
            return HttpResponseNotFound("Anime non trouvé")
        data = response.json().get("data", {})
        if not data:
            return HttpResponseNotFound("Données non valides")

        synopsis_en = data.get("synopsis", "")
        synopsis_fr = safe_translate(synopsis_en)

        anime = Anime.objects.create(
            mal_id=mal_id,
            title=data.get("title"),
            synopsis=synopsis_en,
            synopsis_fr=synopsis_fr,
            image_url=data.get("images", {}).get("jpg", {}).get("image_url"),
            status=data.get("status", ""),
            release_date=parse_date(data.get("aired", {}).get("from"))
        )
        return anime

def create_episodes(anime):
    # D'abord on récupère les infos générales pour avoir la durée
    anime_info = requests.get(f"https://api.jikan.moe/v4/anime/{anime.mal_id}")
    episode_duration_minutes = None

    if anime_info.status_code == 200:
        duration_str = anime_info.json().get("data", {}).get("duration", "")
        if duration_str:
            try:
                # Exemple : "24 min per ep"
                episode_duration_minutes = int(duration_str.split(" ")[0])
            except Exception:
                pass

    base_url = f"https://api.jikan.moe/v4/anime/{anime.mal_id}/episodes"
    page = 1
    episodes_created = 0

    while True:
        response = requests.get(base_url, params={"page": page})
        if response.status_code != 200:
            break

        data = response.json()
        episode_data = data.get("data", [])
        if not episode_data:
            break

        for ep in episode_data:
            aired_str = ep.get("aired")
            air_date = None
            if aired_str:
                try:
                    air_date = datetime.fromisoformat(aired_str).date()
                except Exception:
                    pass

            title_en = ep.get("title", "")
            title_fr = safe_translate(title_en)

            # Évite les doublons si cette fonction est appelée plusieurs fois
            if not Episode.objects.filter(anime=anime, episode_number=ep.get("mal_id")).exists():
                Episode.objects.create(
                    anime=anime,
                    episode_number=ep.get("mal_id"),
                    title=title_en,
                    title_fr=title_fr,
                    air_date=air_date,
                    duration=episode_duration_minutes
                )
                episodes_created += 1

        if not data.get("pagination", {}).get("has_next_page", False):
            break

        page += 1

    total = Episode.objects.filter(anime=anime).count()
    print(total)
    if not total :
        anime.nb_episodes = 1
    else :
        anime.nb_episodes = total
    anime.save() 
            
    

def parse_date(date_str):
    if date_str:
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
        except Exception:
            pass
    return None
