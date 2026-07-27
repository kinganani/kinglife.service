#!/bin/bash
# Créer et activer un environnement virtuel pour éviter l'erreur "externally-managed-environment" de Vercel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --noinput
