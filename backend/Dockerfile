# Étape 1 : Choisir une image Python légère
FROM python:3.12-slim

# Étape 2 : Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Étape 3 : Installer les dépendances système (pour psycopg2, Pillow, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Étape 4 : Copier le fichier requirements.txt
COPY requirements.txt .

# Étape 5 : Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Étape 6 : Copier le reste du code de l’application
COPY . .
RUN chmod +x ./wait-for-it.sh

# Étape 7 : Exposer le port (8000 par défaut)
EXPOSE 8000

# Étape 8 : Lancer Django avec Gunicorn (recommandé)
CMD ["gunicorn", "backend_project.wsgi:application", "--bind", "0.0.0.0:8000"]
#CMD ["./wait-for-it.sh", "db:5432", "--", "gunicorn", "backend_project.wsgi:application", "--bind", "0.0.0.0:8000"]

