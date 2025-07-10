#!/usr/bin/env python3
"""
Script de test pour l'interface admin SocialBoost Pro
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_admin_interface():
    """Test de l'interface admin"""
    print("🧪 Test de l'interface admin SocialBoost Pro")
    print("=" * 50)
    
    # Test de l'endpoint racine
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint racine: OK")
            if "admin" in data:
                print(f"   Interface admin: {data['admin']}")
        else:
            print(f"❌ Endpoint racine: Erreur {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Endpoint racine: Erreur de connexion - {e}")
        return False
    
    # Test de l'interface admin
    try:
        response = requests.get(f"{BASE_URL}/admin")
        if response.status_code == 200:
            print("✅ Interface admin: Accessible")
        else:
            print(f"❌ Interface admin: Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ Interface admin: Erreur de connexion - {e}")
    
    # Test du dashboard admin
    try:
        response = requests.get(f"{BASE_URL}/admin/dashboard")
        if response.status_code == 200:
            print("✅ Dashboard admin: Accessible")
        else:
            print(f"❌ Dashboard admin: Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard admin: Erreur de connexion - {e}")
    
    # Test des statistiques
    try:
        response = requests.get(f"{BASE_URL}/admin/stats")
        if response.status_code == 200:
            print("✅ Statistiques admin: Accessible")
        else:
            print(f"❌ Statistiques admin: Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ Statistiques admin: Erreur de connexion - {e}")
    
    print("\n" + "=" * 50)
    print("📋 Instructions d'accès:")
    print(f"🌐 Interface admin: {BASE_URL}/admin")
    print(f"📊 Dashboard: {BASE_URL}/admin/dashboard")
    print(f"📈 Statistiques: {BASE_URL}/admin/stats")
    print(f"🔐 Connexion admin: admin@socialboostpro.com / admin123")
    print("\n💡 Pour tester l'interface complète:")
    print("1. Ouvrez votre navigateur")
    print("2. Allez sur l'URL de l'interface admin")
    print("3. Connectez-vous avec les credentials admin")
    print("4. Explorez les différentes sections")

def test_admin_api_endpoints():
    """Test des endpoints API admin"""
    print("\n🔐 Test des endpoints API admin")
    print("=" * 40)
    
    # Connexion admin
    login_data = {
        "username": "admin@socialboostpro.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/admin/login", data=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print("✅ Connexion admin: OK")
            print(f"   Token obtenu: {token[:20]}...")
            
            # Test des endpoints protégés
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test plateformes
            response = requests.get(f"{BASE_URL}/admin/platforms", headers=headers)
            if response.status_code == 200:
                platforms = response.json()
                print(f"✅ Plateformes: {len(platforms)} trouvées")
            else:
                print(f"❌ Plateformes: Erreur {response.status_code}")
            
            # Test services
            response = requests.get(f"{BASE_URL}/admin/services", headers=headers)
            if response.status_code == 200:
                services = response.json()
                print(f"✅ Services: {len(services)} trouvés")
            else:
                print(f"❌ Services: Erreur {response.status_code}")
            
            # Test commandes
            response = requests.get(f"{BASE_URL}/orders/admin", headers=headers)
            if response.status_code == 200:
                orders = response.json()
                print(f"✅ Commandes: {len(orders)} trouvées")
            else:
                print(f"❌ Commandes: Erreur {response.status_code}")
            
            # Test paiements
            response = requests.get(f"{BASE_URL}/payments/admin", headers=headers)
            if response.status_code == 200:
                payments = response.json()
                print(f"✅ Paiements: {len(payments)} trouvés")
            else:
                print(f"❌ Paiements: Erreur {response.status_code}")
            
            # Test tickets support
            response = requests.get(f"{BASE_URL}/support/admin", headers=headers)
            if response.status_code == 200:
                tickets = response.json()
                print(f"✅ Tickets support: {len(tickets)} trouvés")
            else:
                print(f"❌ Tickets support: Erreur {response.status_code}")
                
        else:
            print(f"❌ Connexion admin: Erreur {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test API admin: Erreur - {e}")

def main():
    """Fonction principale"""
    print("🚀 Test de l'interface admin SocialBoost Pro")
    print("=" * 60)
    
    # Test de base
    test_admin_interface()
    
    # Test des API
    test_admin_api_endpoints()
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés!")
    print("\n📚 Documentation:")
    print(f"   API: {BASE_URL}/docs")
    print(f"   Admin: {BASE_URL}/admin")
    print(f"   README: Voir le fichier README.md")

if __name__ == "__main__":
    main() 