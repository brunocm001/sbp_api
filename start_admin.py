#!/usr/bin/env python3
"""
Script de démarrage pour l'interface admin SocialBoost Pro
"""
import uvicorn
import subprocess
import sys
import time
import requests
from config import settings

def check_redis():
    """Vérifier si Redis est disponible"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        return True
    except:
        return False

def start_redis():
    """Démarrer Redis si nécessaire"""
    print("🔍 Vérification de Redis...")
    if not check_redis():
        print("⚠️ Redis n'est pas démarré. Tentative de démarrage...")
        try:
            # Essayer de démarrer Redis
            subprocess.Popen(["redis-server"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
            if check_redis():
                print("✅ Redis démarré avec succès")
                return True
            else:
                print("❌ Impossible de démarrer Redis automatiquement")
                print("💡 Veuillez démarrer Redis manuellement:")
                print("   - Linux/Mac: redis-server")
                print("   - Windows: redis-server.exe")
                print("   - Docker: docker run -d -p 6379:6379 redis:7-alpine")
                return False
        except FileNotFoundError:
            print("❌ Redis n'est pas installé")
            print("💡 Installez Redis:")
            print("   - Linux: sudo apt-get install redis-server")
            print("   - Mac: brew install redis")
            print("   - Windows: Téléchargez depuis https://redis.io/download")
            return False
    else:
        print("✅ Redis est déjà démarré")
        return True

def check_database():
    """Vérifier la connexion à la base de données"""
    try:
        from database import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False

def initialize_database():
    """Initialiser la base de données"""
    try:
        print("🗃️ Initialisation de la base de données...")
        subprocess.run([sys.executable, "init_db.py"], check=True)
        print("✅ Base de données initialisée")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Démarrage de l'interface admin SocialBoost Pro")
    print("=" * 60)
    
    # Vérifier Redis
    if not start_redis():
        print("\n❌ Impossible de démarrer sans Redis")
        return
    
    # Vérifier la base de données
    if not check_database():
        print("\n❌ Impossible de se connecter à la base de données")
        print("💡 Vérifiez que PostgreSQL est démarré et configuré")
        return
    
    # Initialiser la base de données si nécessaire
    initialize_database()
    
    print("\n🌐 Démarrage de l'application...")
    print("=" * 60)
    print("📚 Documentation API: http://localhost:8000/docs")
    print("🔧 ReDoc: http://localhost:8000/redoc")
    print("🎛️ Interface Admin: http://localhost:8000/admin")
    print("📊 Dashboard: http://localhost:8000/admin/dashboard")
    print("📈 Statistiques: http://localhost:8000/admin/stats")
    print("=" * 60)
    print("🔐 Connexion admin:")
    print("   Email: admin@socialboostpro.com")
    print("   Mot de passe: admin123")
    print("=" * 60)
    
    # Démarrer l'application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )

if __name__ == "__main__":
    main() 