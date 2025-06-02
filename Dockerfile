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

RUN python manage.py collectstatic --noinput
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh
# Étape 6 : Exposer le port Django
EXPOSE 8000

# Étape 7 : Commande de lancement
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]