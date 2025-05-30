import requests
import json
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Anime, UserAnime

from nikki.utils import get_anime_genres

User = get_user_model()

# --- AUTHENTIFICATION ---

@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"error": "Identifiants invalides"}, status=401)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Données JSON invalides"}, status=400)

@csrf_exempt
def signup(request):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    try:
        data = json.loads(request.body)

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        avatar = data.get("avatar", "")

        if not all([username, email, password]):
            return JsonResponse({"error": "Champs requis manquants"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Nom d'utilisateur déjà pris"}, status=409)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            avatar=avatar
        )

        login(request, user)
        return JsonResponse({"success": True})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Données JSON invalides"}, status=400)

def logout_view(request):
    logout(request)
    return redirect("home")

# --- FRONT ---

def home(request):
    response = requests.get("https://api.jikan.moe/v4/top/anime")
    top_animes = []

    if response.status_code == 200:
        data = response.json()
        top_animes = data.get("data", [])[:10]

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

def all_genres(request):
    genres = get_anime_genres()
    return render(request, "animes/all_genres.html", {
        "anime_genres": genres
    })

@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']
        user.save()
        return JsonResponse({'status': 'ok'})
    return render(request, 'users/profile.html')

@login_required
def delete_data(request):
    if request.method == 'POST':
        user = request.user
        user.email = ''
        if user.avatar:
            user.avatar.delete(save=False)
        user.save()

        # user.anime_notes.all().delete()
        # user.watchlist.clear()

        return JsonResponse({'status': 'ok'})
    
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return JsonResponse({'status': 'deleted'})
    
# --ADD ANIME TO LIST--

@require_POST
@login_required
def add_anime_to_list(request):
    data = json.loads(request.body)

    mal_id = data.get('anime_id')  # ID provenant de Jikan
    status = data.get('status')
    title = data.get('title')
    image_url = data.get('image_url')

    if not (mal_id and status and title):
        return JsonResponse({'error': 'Données manquantes'}, status=400)

    # Crée ou récupère l'anime dans la base
    anime, created = Anime.objects.get_or_create(
        mal_id=mal_id,
        defaults={
            'title': title,
            'image_url': image_url,
            'status': '',  # ou un champ par défaut
            'release_date': None
        }
    )

    # Crée ou met à jour la ligne UserAnime
    ua, created_ua = UserAnime.objects.update_or_create(
        user=request.user,
        anime=anime,
        defaults={'status': status}
    )

    return JsonResponse({'success': True, 'created': created_ua})