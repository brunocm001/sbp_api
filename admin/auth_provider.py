from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.models import AbstractAdmin
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine
from models import Admin
from utils.auth import verify_password
from typing import Optional
import uuid

class CustomLoginProvider(UsernamePasswordProvider):
    """Provider d'authentification personnalisé pour FastAPI Admin"""
    
    async def authenticate(self, username: str, password: str) -> Optional[AbstractAdmin]:
        """Authentification personnalisée avec nos modèles Admin"""
        async with AsyncSession(engine) as session:
            # Rechercher l'admin par email
            admin = await session.execute(
                "SELECT * FROM admins WHERE email = :email",
                {"email": username}
            )
            admin_result = admin.fetchone()
            
            if admin_result and verify_password(password, admin_result.password_hash):
                # Créer un objet admin compatible avec FastAPI Admin
                return AdminAdmin(
                    id=admin_result.id,
                    username=admin_result.email,
                    email=admin_result.email,
                    role=admin_result.role
                )
        return None

class AdminAdmin(AbstractAdmin):
    """Classe admin compatible avec FastAPI Admin"""
    
    def __init__(self, id: str, username: str, email: str, role: str):
        self.id = id
        self.username = username
        self.email = email
        self.role = role
    
    @property
    def is_superuser(self) -> bool:
        """Vérifier si l'admin est super administrateur"""
        return self.role == "superadmin"
    
    @property
    def permissions(self) -> list:
        """Retourner les permissions de l'admin"""
        if self.role == "superadmin":
            return ["*"]  # Toutes les permissions
        elif self.role == "moderator":
            return [
                "platforms:read",
                "services:read", 
                "service_types:read",
                "orders:read",
                "orders:update",
                "payments:read",
                "support_tickets:read",
                "support_tickets:update"
            ]
        return []
    
    async def get_permissions(self) -> list:
        """Méthode requise par FastAPI Admin"""
        return self.permissions 