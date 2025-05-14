import requests

def get_anime_genres():
    try:
        response = requests.get("https://api.jikan.moe/v4/genres/anime", timeout=5)
        if response.status_code == 200:
            return response.json().get("data", [])
    except Exception as e:
        print("Erreur chargement des genres :", e)
    return []