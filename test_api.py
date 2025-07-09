#!/usr/bin/env python3
"""
Script de test simple pour vérifier que l'API fonctionne
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test de l'endpoint de santé"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check: OK")
            return True
        else:
            print(f"❌ Health check: Erreur {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check: Erreur de connexion - {e}")
        return False

def test_root():
    """Test de l'endpoint racine"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Root endpoint: OK")
            print(f"   Message: {data.get('message')}")
            return True
        else:
            print(f"❌ Root endpoint: Erreur {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint: Erreur de connexion - {e}")
        return False

def test_docs():
    """Test de l'endpoint de documentation"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Documentation: OK")
            return True
        else:
            print(f"❌ Documentation: Erreur {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Documentation: Erreur de connexion - {e}")
        return False

def test_admin_login():
    """Test de la connexion admin"""
    try:
        login_data = {
            "username": "admin@socialboostpro.com",
            "password": "admin123"
        }
        response = requests.post(f"{BASE_URL}/admin/login", data=login_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ Admin login: OK")
            print(f"   Token type: {data.get('token_type')}")
            return data.get('access_token')
        else:
            print(f"❌ Admin login: Erreur {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Admin login: Erreur de connexion - {e}")
        return None

def test_platforms(token):
    """Test de l'endpoint des plateformes"""
    if not token:
        print("❌ Test plateformes: Pas de token")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/admin/platforms", headers=headers)
        if response.status_code == 200:
            platforms = response.json()
            print(f"✅ Plateformes: OK ({len(platforms)} plateformes trouvées)")
            for platform in platforms:
                print(f"   - {platform.get('name')}")
            return True
        else:
            print(f"❌ Plateformes: Erreur {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Plateformes: Erreur de connexion - {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 Tests de l'API SocialBoost Pro")
    print("=" * 40)
    
    # Tests de base
    health_ok = test_health()
    root_ok = test_root()
    docs_ok = test_docs()
    
    if not all([health_ok, root_ok, docs_ok]):
        print("\n❌ Tests de base échoués. Vérifiez que l'application est démarrée.")
        return
    
    print("\n🔐 Tests d'authentification...")
    token = test_admin_login()
    
    if token:
        print("\n📊 Tests des endpoints admin...")
        test_platforms(token)
    
    print("\n" + "=" * 40)
    print("✅ Tests terminés!")
    print(f"📚 Documentation: {BASE_URL}/docs")
    print(f"🔧 ReDoc: {BASE_URL}/redoc")

if __name__ == "__main__":
    main() 