# Nikki Anime Tracker

Nikki est une application web écrite en **Django** qui permet de suivre vos animes favoris.
Elle propose l'authentification par e-mail, la gestion de listes personnalisées et le suivi des épisodes vus.

## Fonctionnalités
- Inscription et connexion des utilisateurs
- Consultation des animes en tendance (données externes)
- Classement des animes par genre
- Ajout d'un anime à sa liste personnelle avec un statut (à voir, en cours, terminé)
- Marquage des épisodes vus et suivi automatique de la progression

## Stack technique
- Python 3.10 et Django 5
- PostgreSQL pour la persistance des données
- Playwright pour les tests end‑to‑end
- Docker & Docker Compose (optionnel)

## Prérequis
- Python 3.10 ou plus
- PostgreSQL
- (Optionnel) Docker et Docker-Compose pour un déploiement simplifié

## Installation
1. Clonez ce dépôt puis placez vous dans le dossier du projet:
   ```bash
   git clone <repo-url>
   cd Nikki_animeTracker
   ```
2. Installez les dépendances Python (recommandé dans un environnement virtuel):
   ```bash
   pip install -r requirements.txt
   ```
3. Créez un fichier `.env` à la racine en vous basant sur les variables ci-dessous.

### Variables d'environnement principales
```
DB_NAME=nikki_db
DB_USER=nikki_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=change-me
DEBUG=1
ALLOWED_HOSTS=localhost
```

## Lancement de l'application
### Avec Docker
```bash
docker-compose up --build
```
L'application sera disponible sur [http://localhost:8000] et la base PostgreSQL sur le port `5433`.

### En local
Assurez-vous que PostgreSQL tourne et que la base renseignée dans `.env` existe.
```bash
python manage.py migrate
python manage.py runserver
```

## Lancement des tests
La suite de tests se lance avec `pytest`.
Pour les tests end‑to‑end utilisant Playwright, exécutez d'abord :
```bash
playwright install
```
Ensuite:
```bash
pytest
```

## Structure du projet
- `config/` : configuration Django
- `nikki/` : application principale (modèles, vues, templates)
- `docker-compose.yml` et `Dockerfile` : environnements Docker

## Principaux modèles
- `User` : utilisateur avec adresse e-mail unique et avatar
- `Anime` : fiche anime récupérée depuis Jikan
- `UserAnime` : lien entre un utilisateur et un anime (statut, note)
- `Episode` : épisodes d'un anime avec traduction française
- `UserEpisodeView` : suivi des épisodes vus par utilisateur

## Principaux endpoints
Liste (non exhaustive) des routes exposées par l'application :

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/` | Page d'accueil avec les tendances |
| POST | `/signup/` | Inscription d'un utilisateur |
| POST | `/login/` | Connexion (JSON) |
| GET | `/logout/` | Déconnexion |
| GET/POST | `/profil/` | Gestion du profil |
| POST | `/supprimer-compte/` | Suppression du compte |
| POST | `/supprimer-donnees/` | Anonymisation des données |
| GET | `/animes/` | Recherche et listing des animes |
| GET | `/anime/<id>/` | Détail d'un anime |
| GET | `/genres/` | Liste des genres |
| GET | `/genres/<slug>/` | Animes par genre |
| POST | `/add-to-list/` | Ajout d'un anime à la liste |
| POST | `/ajax/change-anime-status/` | Changer le statut d'un anime |
| POST | `/remove-anime/<id>/` | Retrait d'un anime de la liste |
| POST | `/toggle-episode/` | Marquer un épisode vu |
| GET | `/conditions-utilisation/` | Conditions d'utilisation |
| GET | `/politique-confidentialite/` | Politique de confidentialité |
| GET | `/admin/` | Interface d'administration |

## Authentification
L'application repose sur le système de sessions de Django avec un modèle `User` personnalisé.
- Les routes `/signup/` et `/login/` reçoivent des données JSON pour créer un compte ou se connecter.
- Le champ `email` sert d'identifiant unique pour la connexion.
- Les vues de gestion de profil ou de liste sont protégées par le décorateur `@login_required`.

## Contribuer
Les contributions sont les bienvenues ! Ouvrez une issue ou une pull request pour proposer vos améliorations.