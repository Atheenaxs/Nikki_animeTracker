# Étape 1: Utiliser une image de base officielle Python
FROM python:3.10-slim

# Étape 2: Installer gcc et autres dépendances nécessaires (comme libpq-dev pour PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    g++ \
    make && \
    rm -rf /var/lib/apt/lists/*  # Nettoyer les caches pour réduire la taille de l'image

# Étape 3: Définir le répertoire de travail dans le container
WORKDIR /app

# Étape 4: Copier le fichier requirements.txt et installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5: Copier le reste des fichiers de l'application
COPY . /app/

# Étape 6: Exposer le port sur lequel l'application va écouter
EXPOSE 8000

# Étape 7: Lancer le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
