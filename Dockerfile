# Étape 1 : Image de base légère avec Python 3.10
FROM python:3.10-slim

# Étape 2 : Installer les dépendances système utiles (libpq-dev pour psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Étape 3 : Définir le dossier de travail
WORKDIR /app

# Étape 4 : Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copier le reste du code
COPY . .

# Étape 6 : Rendre le script wait-for-it exécutable (si utilisé)
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Étape 7 : Exposer le port utilisé par Django/WSGI
EXPOSE 8000

# Étape 8 : Lancer collectstatic + serveur WSGI (gunicorn recommandé en prod)
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
