import requests
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Anime, Episode, UserAnime, UserEpisodeView
from nikki.utils import get_anime_genres, get_or_create_anime_or_404, create_episodes
from django.http import HttpResponseNotFound

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

    to_watch = UserAnime.objects.filter(user=request.user, status='toWatch').select_related('anime')
    watching = UserAnime.objects.filter(user=request.user, status='watching').select_related('anime')
    finished = UserAnime.objects.filter(user=request.user, status='finished').select_related('anime')

    anime_lists = [
        ("À voir plus tard", to_watch),
        ("En cours", watching),
        ("Terminés", finished),
    ]

    return render(request, 'users/profile.html', {
        'anime_lists': anime_lists,
        'to_watch': to_watch,
        'watching': watching,
        'finished': finished,
    })


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
    if created:
        from .utils import create__episodes
        create__episodes(anime)
        anime.refresh_from_db()

    # Crée ou met à jour la ligne UserAnime
    ua, created_ua = UserAnime.objects.update_or_create(
        user=request.user,
        anime=anime,
        defaults={'status': status}
    )

    # Si l'utilisateur choisit "finished", marquer tous les épisodes comme vus
    if status == 'finished':
        from .models import Episode, UserEpisodeView

        episodes = Episode.objects.filter(anime=anime)
        for ep in episodes:
            ep_view, _ = UserEpisodeView.objects.get_or_create(user=request.user, episode=ep)
            ep_view.is_watched = True
            ep_view.save()

    return JsonResponse({'success': True, 'created': created_ua})

@require_POST
@login_required
@csrf_exempt
def change_anime_status_ajax(request):
    import json
    data = json.loads(request.body)
    anime_id = data.get("user_anime_id")
    new_status = data.get("new_status")

    if new_status not in dict(UserAnime.STATUS_CHOICES):
        return JsonResponse({"error": "Statut invalide"}, status=400)

    ua = get_object_or_404(UserAnime, id=anime_id, user=request.user)
    ua.status = new_status
    ua.save()

    return JsonResponse({"success": True})

@login_required
def remove_anime(request, user_anime_id):
    user_anime = get_object_or_404(UserAnime, id=user_anime_id, user=request.user)
    anime = user_anime.anime

    # Supprimer l'entrée UserAnime
    user_anime.delete()

    # Décoche tous les épisodes liés (option 1 : supprimer les vues)
    UserEpisodeView.objects.filter(
        user=request.user,
        episode__anime=anime
    ).delete()

    # (option 2 : décocher sans supprimer)
    # views = UserEpisodeView.objects.filter(user=request.user, episode__anime=anime)
    # for view in views:
    #     view.is_watched = False
    #     view.save()

    return JsonResponse({'success': True})
    
    
def anime_detail(request, anime_id):
    anime = get_or_create_anime_or_404(request, anime_id)
    if isinstance(anime, HttpResponseNotFound):
        return anime

    if not Episode.objects.filter(anime=anime).exists():
        create_episodes(anime)
        anime.refresh_from_db()  # met à jour nb_episodes

    episodes = []
    seen_episode_ids = []
    user_anime = None
    user_anime_status = None

    if anime.nb_episodes > 1:
        episodes = Episode.objects.filter(anime=anime).order_by("episode_number")

        if request.user.is_authenticated:
            user_anime = UserAnime.objects.filter(user=request.user, anime=anime).first()
            user_anime_status = user_anime.status if user_anime else None

            if user_anime and user_anime.status == 'finished':
                seen_episode_ids = list(episodes.values_list("id", flat=True))
            else:
                seen_episode_ids = list(
                    UserEpisodeView.objects.filter(
                        user=request.user,
                        episode__in=episodes,
                        is_watched=True
                    ).values_list("episode__id", flat=True)
                )
    else:
        if request.user.is_authenticated:
            user_anime = UserAnime.objects.filter(user=request.user, anime=anime).first()
            user_anime_status = user_anime.status if user_anime else None

    return render(request, 'animes/anime_detail.html', {
        'anime': anime,
        'episodes': episodes,
        'seen_episode_ids': seen_episode_ids,
        'user_anime': user_anime,
        'user_anime_status': user_anime_status,
    })


@login_required
def toggle_episode_view(request):
    data = json.loads(request.body)
    episode_id = data.get('episode_id')
    watched = str(data.get('watched', 'false')).lower() == 'true'

    episode = get_object_or_404(Episode, pk=episode_id)
    anime = episode.anime

    # Met à jour la vue de l’épisode
    ep_view, _ = UserEpisodeView.objects.get_or_create(user=request.user, episode=episode)
    ep_view.is_watched = watched
    ep_view.save()

    # Compte le nombre d’épisodes vus
    total_eps = anime.nb_episodes or 1
    seen_eps = UserEpisodeView.objects.filter(
        user=request.user,
        episode__anime=anime,
        is_watched=True
    ).count()

    ua, _ = UserAnime.objects.get_or_create(user=request.user, anime=anime)

    # Ne touche pas aux autres épisodes ! On met juste à jour le statut
    if seen_eps == total_eps:
        ua.status = 'finished'
    else:
        ua.status = 'watching'
    ua.save()

    return JsonResponse({"success": True})


