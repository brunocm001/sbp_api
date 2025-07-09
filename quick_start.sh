#!/bin/bash

echo "🚀 Démarrage rapide de SocialBoost Pro"
echo "======================================"

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si pip est installé
if ! command -v pip &> /dev/null; then
    echo "❌ pip n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Créer un environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📚 Installation des dépendances..."
pip install -r requirements.txt

# Vérifier si PostgreSQL est installé et en cours d'exécution
echo "🗄️ Vérification de PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo "⚠️ PostgreSQL n'est pas installé. Vous devrez l'installer manuellement."
    echo "Ou utilisez Docker avec: docker-compose up -d"
else
    echo "✅ PostgreSQL détecté"
fi

# Initialiser la base de données
echo "🗃️ Initialisation de la base de données..."
python init_db.py

# Démarrer l'application
echo "🚀 Démarrage de l'application..."
echo "======================================"
echo "📚 Documentation: http://localhost:8000/docs"
echo "🔧 ReDoc: http://localhost:8000/redoc"
echo "🔐 Admin: admin@socialboostpro.com / admin123"
echo "======================================"

python start.py 