# Dockerfile pour application Python Flask
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances et installer
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code backend
COPY backend/ .

# Exposer le port par défaut de Flask
EXPOSE 5000

# Commande de lancement
CMD ["python", "app.py"]
