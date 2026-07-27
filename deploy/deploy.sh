#!/bin/bash
# ==========================================================================
# AUTOMATED DEPLOYMENT SCRIPT FOR KINGLIFE SHAL U (LINUX UBUNTU VPS)
# ==========================================================================

set -e

echo "[1/5] Pulling latest code from GitHub..."
git pull origin main

echo "[2/5] Installing Python dependencies..."
source env/bin/activate
pip install -r requirements.txt

echo "[3/5] Running Database Migrations..."
python manage.py migrate
python manage.py seed_data

echo "[4/5] Collecting Static Files..."
python manage.py collectstatic --noinput

echo "[5/5] Restarting Gunicorn & Nginx Services..."
sudo systemctl restart gunicorn_kinglife
sudo systemctl reload nginx

echo "✅ KINGLIFE SHAL U Web Platform successfully deployed!"
