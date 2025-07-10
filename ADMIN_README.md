# Interface d'Administration SocialBoost Pro

Interface d'administration complète et sécurisée pour SocialBoost Pro, construite avec FastAPI Admin.

## 🎯 Fonctionnalités

### 📊 Dashboard
- **Vue d'ensemble** : Statistiques en temps réel
- **Graphiques interactifs** : Évolution des commandes et revenus
- **Métriques clés** : Commandes, CA, tickets support
- **Dernières activités** : Commandes et tickets récents

### 🔧 Gestion des données
- **Plateformes** : CRUD complet (YouTube, TikTok, Instagram, Facebook)
- **Services** : Gestion des services par plateforme
- **Types de services** : Configuration des prix et délais
- **Commandes** : Suivi et modification des statuts
- **Paiements** : Gestion des transactions
- **Support** : Réponse aux tickets clients
- **Administrateurs** : Gestion des comptes admin

### 🔐 Sécurité
- **Authentification JWT** : Connexion sécurisée
- **Rôles et permissions** : Super admin et modérateur
- **Sessions sécurisées** : Gestion Redis
- **Validation des données** : Pydantic schemas

## 🚀 Installation

### Prérequis
- Python 3.8+
- PostgreSQL
- Redis (pour les sessions)

### Installation rapide

#### Option 1 : Docker (Recommandé)
```bash
# Avec Redis pour l'interface admin
docker-compose -f docker-compose.admin.yml up -d

# Ou version standard
docker-compose up -d
```

#### Option 2 : Installation manuelle
```bash
# Installer les dépendances
pip install -r requirements.txt

# Démarrer Redis (nécessaire pour FastAPI Admin)
redis-server

# Initialiser la base de données
python init_db.py

# Démarrer l'application
python start.py
```

## 🔑 Accès

### Credentials par défaut
- **URL** : http://localhost:8000/admin
- **Email** : admin@socialboostpro.com
- **Mot de passe** : admin123

### Rôles disponibles
- **Super Admin** : Accès complet à toutes les fonctionnalités
- **Modérateur** : Accès limité (lecture + modification commandes/support)

## 📱 Interface utilisateur

### Navigation
- **Dashboard** : Vue d'ensemble et statistiques
- **Configuration** : Plateformes, services, types
- **Commandes** : Gestion des commandes et paiements
- **Support** : Tickets de support
- **Administrateurs** : Gestion des comptes
- **Statistiques** : Rapports détaillés

### Fonctionnalités par section

#### 🏠 Dashboard
- Statistiques en temps réel
- Graphiques d'évolution
- Dernières commandes
- Tickets support récents
- Métriques de performance

#### ⚙️ Configuration
- **Plateformes** : Ajout/modification des réseaux sociaux
- **Services** : Gestion des types de services (vues, likes, abonnés)
- **Types de services** : Configuration des prix et délais

#### 📦 Commandes
- **Liste des commandes** : Filtres par statut, date, plateforme
- **Détails commande** : Informations complètes
- **Modification statut** : Mise à jour en temps réel
- **Suivi progression** : Barre de progression

#### 💳 Paiements
- **Liste des paiements** : Filtres par méthode, statut
- **Détails transaction** : Informations de paiement
- **Modification statut** : Validation/refus des paiements

#### 🎧 Support
- **Tickets ouverts** : Liste des demandes en attente
- **Réponse aux tickets** : Interface de réponse intégrée
- **Historique** : Suivi des conversations
- **Fermeture** : Résolution des tickets

#### 👥 Administrateurs
- **Liste des admins** : Gestion des comptes
- **Création de comptes** : Ajout de nouveaux administrateurs
- **Gestion des rôles** : Attribution des permissions
- **Modification des profils** : Mise à jour des informations

## 🔧 Configuration

### Variables d'environnement
```env
# Base de données
DATABASE_URL=postgresql://username:password@localhost:5432/socialboost_pro

# Redis (pour les sessions admin)
REDIS_URL=redis://localhost:6379/0

# Sécurité
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
ALLOWED_HOSTS=["*"]

# Admin par défaut
ADMIN_EMAIL=admin@socialboostpro.com
ADMIN_PASSWORD=admin123
```

### Personnalisation
- **Logo** : Modifier `admin/config.py` - `logo_url`
- **Thème** : Personnaliser `static/css/admin.css`
- **Templates** : Modifier les fichiers dans `templates/admin/`

## 📊 API Endpoints

### Public (sans authentification)
- `GET /admin` - Interface admin
- `GET /admin/dashboard` - Dashboard
- `GET /admin/stats` - Statistiques

### Admin (authentification requise)
- `POST /admin/login` - Connexion
- `GET /admin/me` - Profil admin
- `POST /admin/register` - Créer un admin

### CRUD Endpoints
- `GET/POST/PUT/DELETE /admin/platforms` - Gestion plateformes
- `GET/POST/PUT/DELETE /admin/services` - Gestion services
- `GET/POST/PUT/DELETE /admin/service-types` - Gestion types
- `GET/PUT /admin/orders` - Gestion commandes
- `GET/PUT /admin/payments` - Gestion paiements
- `GET/PUT /admin/support-tickets` - Gestion support
- `GET/POST/PUT/DELETE /admin/admins` - Gestion admins

## 🧪 Tests

### Test de l'interface
```bash
python test_admin.py
```

### Test manuel
1. Ouvrir http://localhost:8000/admin
2. Se connecter avec les credentials admin
3. Explorer les différentes sections
4. Tester les fonctionnalités CRUD

## 🔒 Sécurité

### Authentification
- **JWT Tokens** : Authentification sécurisée
- **Hachage des mots de passe** : bcrypt
- **Sessions Redis** : Gestion des sessions
- **Expiration automatique** : Tokens temporaires

### Permissions
- **Super Admin** : Accès complet
- **Modérateur** : Accès limité
- **Validation des données** : Pydantic schemas
- **Protection CSRF** : Intégrée

### Bonnes pratiques
- Changer le mot de passe admin par défaut
- Utiliser HTTPS en production
- Configurer Redis avec authentification
- Limiter les tentatives de connexion

## 🚀 Déploiement

### Production
```bash
# Variables d'environnement
export DATABASE_URL="postgresql://..."
export REDIS_URL="redis://..."
export SECRET_KEY="your-production-secret"

# Démarrer avec Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker Production
```bash
# Build de l'image
docker build -t socialboost-pro-admin .

# Démarrer avec docker-compose
docker-compose -f docker-compose.admin.yml up -d
```

## 📝 Logs et monitoring

### Logs
- **Application** : stdout/stderr
- **Base de données** : PostgreSQL logs
- **Redis** : Redis logs
- **Nginx** : Access/error logs

### Monitoring
- **Health check** : `GET /health`
- **Métriques** : Dashboard intégré
- **Alertes** : Configuration personnalisable

## 🆘 Support

### Problèmes courants
1. **Redis non connecté** : Vérifier que Redis est démarré
2. **Base de données** : Vérifier la connexion PostgreSQL
3. **Permissions** : Vérifier les droits d'accès
4. **Ports** : Vérifier que les ports 8000 et 6379 sont libres

### Debug
```bash
# Mode debug
export DEBUG=True
python start.py

# Logs détaillés
uvicorn main:app --log-level debug
```

## 📚 Documentation

- **API** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
- **Admin** : http://localhost:8000/admin
- **README principal** : README.md

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature
3. Implémenter les changements
4. Tester l'interface admin
5. Créer une Pull Request

---

**SocialBoost Pro Admin** - Interface d'administration complète et sécurisée 