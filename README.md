# SocialBoost Pro - API Backend

Une application FastAPI complète pour gérer des services de boost sur les réseaux sociaux (vues, likes, abonnés, etc.).

## 🚀 Fonctionnalités

- **Gestion des plateformes** : YouTube, TikTok, Instagram, Facebook
- **Services personnalisables** : Vues, likes, abonnés, etc.
- **Types de services** : Différentes qualités et prix
- **Commandes** : Système de commande complet
- **Paiements** : Intégration avec différents moyens de paiement
- **Support** : Système de tickets de support
- **Administration** : Interface admin sécurisée avec JWT
- **API REST** : Documentation automatique avec Swagger UI

## 🛠️ Technologies

- **FastAPI** : Framework web moderne et rapide
- **SQLAlchemy** : ORM pour la gestion de la base de données
- **PostgreSQL** : Base de données relationnelle
- **Alembic** : Migrations de base de données
- **JWT** : Authentification sécurisée
- **Pydantic** : Validation des données
- **Uvicorn** : Serveur ASGI

## 📋 Prérequis

- Python 3.8+
- PostgreSQL
- pip

## 🔧 Installation

1. **Cloner le projet**
```bash
git clone <repository-url>
cd SocialBoostPro
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer la base de données**
   - Créer une base de données PostgreSQL
   - Modifier le fichier `config.py` avec vos paramètres de connexion

5. **Initialiser la base de données**
```bash
python init_db.py
```

6. **Lancer l'application**
```bash
python main.py
```

L'application sera accessible sur `http://localhost:8000`

## 📚 Documentation API

Une fois l'application lancée, vous pouvez accéder à :

- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`
- **Interface Admin** : `http://localhost:8000/admin`
- **Dashboard Admin** : `http://localhost:8000/admin/dashboard`

## 🔐 Authentification Admin

L'admin par défaut est créé automatiquement :
- **Email** : `admin@socialboostpro.com`
- **Mot de passe** : `admin123`

### Interface Admin Web
Pour accéder à l'interface d'administration complète :
1. Aller sur `http://localhost:8000/admin`
2. Se connecter avec les credentials admin
3. Explorer le dashboard et les différentes sections

### API REST
Pour utiliser l'API REST :
1. Aller sur `http://localhost:8000/docs`
2. Cliquer sur "Authorize" en haut à droite
3. Utiliser l'endpoint `/admin/login` avec les credentials

## 🗄️ Structure de la base de données

### Tables principales :

1. **platforms** : Plateformes sociales (YouTube, TikTok, etc.)
2. **services** : Services proposés (vues, likes, abonnés)
3. **service_types** : Types de services avec prix et délais
4. **orders** : Commandes des clients
5. **payments** : Paiements associés aux commandes
6. **support_tickets** : Tickets de support
7. **admins** : Administrateurs du système

## 🔄 Migrations

Pour créer une nouvelle migration :
```bash
alembic revision --autogenerate -m "Description de la migration"
alembic upgrade head
```

## 📁 Structure du projet

```
SocialBoostPro/
├── alembic/                 # Migrations Alembic
├── models/                  # Modèles SQLAlchemy
│   ├── __init__.py
│   ├── platform.py
│   ├── service.py
│   ├── service_type.py
│   ├── order.py
│   ├── payment.py
│   ├── support_ticket.py
│   └── admin.py
├── schemas/                 # Schémas Pydantic
│   ├── __init__.py
│   ├── platform.py
│   ├── service.py
│   ├── service_type.py
│   ├── order.py
│   ├── payment.py
│   ├── support_ticket.py
│   ├── admin.py
│   └── auth.py
├── routers/                 # Routeurs FastAPI
│   ├── __init__.py
│   ├── platforms.py
│   ├── services.py
│   ├── service_types.py
│   ├── orders.py
│   ├── payments.py
│   ├── support.py
│   └── admin.py
├── utils/                   # Utilitaires
│   ├── __init__.py
│   └── auth.py
├── config.py               # Configuration
├── database.py             # Configuration base de données
├── main.py                 # Application principale
├── init_db.py              # Script d'initialisation
├── requirements.txt        # Dépendances
├── alembic.ini            # Configuration Alembic
└── README.md              # Documentation
```

## 🚀 Endpoints principaux

### Public
- `POST /orders` : Créer une commande
- `GET /orders/{order_id}` : Suivre une commande
- `POST /payments/initiate` : Initier un paiement
- `POST /payments/verify` : Vérifier un paiement
- `POST /support` : Créer un ticket de support

### Admin (authentification requise)
- `POST /admin/login` : Connexion admin
- `GET /admin/me` : Informations admin connecté
- `POST /admin/register` : Créer un nouvel admin

#### Gestion des plateformes
- `GET /admin/platforms` : Lister les plateformes
- `POST /admin/platforms` : Créer une plateforme
- `PUT /admin/platforms/{id}` : Modifier une plateforme
- `DELETE /admin/platforms/{id}` : Supprimer une plateforme

#### Gestion des services
- `GET /admin/services` : Lister les services
- `POST /admin/services` : Créer un service
- `PUT /admin/services/{id}` : Modifier un service
- `DELETE /admin/services/{id}` : Supprimer un service

#### Gestion des types de services
- `GET /admin/service-types` : Lister les types de services
- `POST /admin/service-types` : Créer un type de service
- `PUT /admin/service-types/{id}` : Modifier un type de service
- `DELETE /admin/service-types/{id}` : Supprimer un type de service

#### Gestion des commandes
- `GET /orders/admin` : Lister les commandes (admin)
- `PUT /orders/admin/{id}/status` : Mettre à jour le statut d'une commande

#### Gestion des paiements
- `GET /payments/admin` : Lister les paiements (admin)
- `PUT /payments/admin/{id}/status` : Mettre à jour le statut d'un paiement

#### Gestion du support
- `GET /support/admin` : Lister les tickets (admin)
- `GET /support/admin/{id}` : Voir un ticket (admin)
- `PUT /support/admin/{id}` : Répondre à un ticket (admin)

## 🔧 Configuration

Modifiez le fichier `config.py` pour adapter la configuration à votre environnement :

```python
# Exemple de configuration
DATABASE_URL = "postgresql://username:password@localhost:5432/socialboost_pro"
SECRET_KEY = "your-super-secret-key-change-in-production"
```

## 🧪 Tests

Pour exécuter les tests (à implémenter) :
```bash
pytest
```

## 📝 Variables d'environnement

Créez un fichier `.env` avec les variables suivantes :

```env
DATABASE_URL=postgresql://username:password@localhost:5432/socialboost_pro
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=SocialBoost Pro
DEBUG=True
ALLOWED_HOSTS=["*"]
ADMIN_EMAIL=admin@socialboostpro.com
ADMIN_PASSWORD=admin123
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème, veuillez ouvrir une issue sur GitHub. 