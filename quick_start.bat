@echo off
echo 🚀 Démarrage rapide de SocialBoost Pro
echo ======================================

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé. Veuillez l'installer d'abord.
    pause
    exit /b 1
)

REM Vérifier si pip est installé
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip n'est pas installé. Veuillez l'installer d'abord.
    pause
    exit /b 1
)

REM Créer un environnement virtuel s'il n'existe pas
if not exist "venv" (
    echo 📦 Création de l'environnement virtuel...
    python -m venv venv
)

REM Activer l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances
echo 📚 Installation des dépendances...
pip install -r requirements.txt

REM Vérifier si PostgreSQL est installé
echo 🗄️ Vérification de PostgreSQL...
psql --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ PostgreSQL n'est pas installé. Vous devrez l'installer manuellement.
    echo Ou utilisez Docker avec: docker-compose up -d
) else (
    echo ✅ PostgreSQL détecté
)

REM Initialiser la base de données
echo 🗃️ Initialisation de la base de données...
python init_db.py

REM Démarrer l'application
echo 🚀 Démarrage de l'application...
echo ======================================
echo 📚 Documentation: http://localhost:8000/docs
echo 🔧 ReDoc: http://localhost:8000/redoc
echo 🔐 Admin: admin@socialboostpro.com / admin123
echo ======================================

python start.py
pause 