#!/usr/bin/env python3
"""
Script pour initialiser la base de données avec des données de test
"""
import uuid
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Platform, Service, ServiceType, Admin
from utils.auth import get_password_hash
from config import settings

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Platform).first():
            print("Base de données déjà initialisée")
            return
        
        # Create platforms
        platforms = [
            Platform(
                id=uuid.uuid4(),
                name="YouTube",
                icon_url="https://example.com/youtube-icon.png",
                is_active=True
            ),
            Platform(
                id=uuid.uuid4(),
                name="TikTok",
                icon_url="https://example.com/tiktok-icon.png",
                is_active=True
            ),
            Platform(
                id=uuid.uuid4(),
                name="Instagram",
                icon_url="https://example.com/instagram-icon.png",
                is_active=True
            ),
            Platform(
                id=uuid.uuid4(),
                name="Facebook",
                icon_url="https://example.com/facebook-icon.png",
                is_active=True
            )
        ]
        
        for platform in platforms:
            db.add(platform)
        db.commit()
        
        # Create services
        services = [
            Service(
                id=uuid.uuid4(),
                platform_id=platforms[0].id,  # YouTube
                name="Vues YouTube",
                description="Augmentation du nombre de vues sur vos vidéos YouTube",
                is_active=True
            ),
            Service(
                id=uuid.uuid4(),
                platform_id=platforms[0].id,  # YouTube
                name="Abonnés YouTube",
                description="Augmentation du nombre d'abonnés sur votre chaîne YouTube",
                is_active=True
            ),
            Service(
                id=uuid.uuid4(),
                platform_id=platforms[1].id,  # TikTok
                name="Vues TikTok",
                description="Augmentation du nombre de vues sur vos vidéos TikTok",
                is_active=True
            ),
            Service(
                id=uuid.uuid4(),
                platform_id=platforms[1].id,  # TikTok
                name="Followers TikTok",
                description="Augmentation du nombre de followers sur votre compte TikTok",
                is_active=True
            ),
            Service(
                id=uuid.uuid4(),
                platform_id=platforms[2].id,  # Instagram
                name="Followers Instagram",
                description="Augmentation du nombre de followers sur votre compte Instagram",
                is_active=True
            ),
            Service(
                id=uuid.uuid4(),
                platform_id=platforms[2].id,  # Instagram
                name="Likes Instagram",
                description="Augmentation du nombre de likes sur vos posts Instagram",
                is_active=True
            )
        ]
        
        for service in services:
            db.add(service)
        db.commit()
        
        # Create service types
        service_types = [
            # YouTube Vues
            ServiceType(
                id=uuid.uuid4(),
                service_id=services[0].id,
                name="Qualité Standard",
                price_per_1000=2.50,
                min_quantity=1000,
                max_quantity=10000,
                delivery_time="24-48 heures",
                guarantee=True,
                description="Vues de qualité standard",
                is_active=True
            ),
            ServiceType(
                id=uuid.uuid4(),
                service_id=services[0].id,
                name="Qualité Premium",
                price_per_1000=5.00,
                min_quantity=1000,
                max_quantity=5000,
                delivery_time="12-24 heures",
                guarantee=True,
                description="Vues de qualité premium avec engagement",
                is_active=True
            ),
            # YouTube Abonnés
            ServiceType(
                id=uuid.uuid4(),
                service_id=services[1].id,
                name="Abonnés Réels",
                price_per_1000=15.00,
                min_quantity=100,
                max_quantity=1000,
                delivery_time="48-72 heures",
                guarantee=True,
                description="Abonnés réels avec profil complet",
                is_active=True
            ),
            # TikTok Vues
            ServiceType(
                id=uuid.uuid4(),
                service_id=services[2].id,
                name="Vues Rapides",
                price_per_1000=1.50,
                min_quantity=1000,
                max_quantity=50000,
                delivery_time="6-12 heures",
                guarantee=True,
                description="Vues rapides pour TikTok",
                is_active=True
            ),
            # TikTok Followers
            ServiceType(
                id=uuid.uuid4(),
                service_id=services[3].id,
                name="Followers Actifs",
                price_per_1000=8.00,
                min_quantity=100,
                max_quantity=2000,
                delivery_time="24-48 heures",
                guarantee=True,
                description="Followers actifs avec engagement",
                is_active=True
            ),
            # Instagram Followers
            ServiceType(
                id=uuid.uuid4(),
                service_id=services[4].id,
                name="Followers Organiques",
                price_per_1000=12.00,
                min_quantity=100,
                max_quantity=1500,
                delivery_time="48-72 heures",
                guarantee=True,
                description="Followers organiques avec profil réel",
                is_active=True
            ),
            # Instagram Likes
            ServiceType(
                id=uuid.uuid4(),
                service_id=services[5].id,
                name="Likes Rapides",
                price_per_1000=3.00,
                min_quantity=100,
                max_quantity=10000,
                delivery_time="1-2 heures",
                guarantee=True,
                description="Likes rapides sur vos posts",
                is_active=True
            )
        ]
        
        for service_type in service_types:
            db.add(service_type)
        db.commit()
        
        # Create default admin
        admin = Admin(
            id=uuid.uuid4(),
            email=settings.admin_email,
            password_hash=get_password_hash(settings.admin_password),
            role="superadmin"
        )
        db.add(admin)
        db.commit()
        
        print("Base de données initialisée avec succès!")
        print(f"Admin créé: {settings.admin_email} / {settings.admin_password}")
        
    except Exception as e:
        print(f"Erreur lors de l'initialisation: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 