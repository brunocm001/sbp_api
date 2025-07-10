from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.resources import Link
from fastapi_admin.models import AbstractAdmin
from fastapi_admin.file_upload import FileUpload
from sqlalchemy.ext.asyncio import AsyncSession
from redis import asyncio as aioredis
from database import engine
from models import Admin
from utils.auth import verify_password
from typing import Optional
import os

# Configuration de l'upload de fichiers
file_upload = FileUpload(uploads_dir="static/uploads")

# Provider d'authentification personnalisé
class CustomLoginProvider(UsernamePasswordProvider):
    async def authenticate(self, username: str, password: str) -> Optional[AbstractAdmin]:
        async with AsyncSession(engine) as session:
            admin = await session.get(Admin, username)
            if admin and verify_password(password, admin.password_hash):
                return admin
        return None

# ✅ Fonction async d'initialisation de l'app
async def create_app():
    # Connexion Redis
    redis1 = aioredis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"), decode_responses=True)

    # Configuration FastAPI Admin
    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=["templates"],
        providers=[
            CustomLoginProvider(
                login_logo_url="https://preview.tabler.io/static/logo.svg",
                admin_model=Admin,
            )
        ],
        redis=redis1,
    )

    # Import et enregistrement des ressources admin
    from models import (
        PlatformAdmin,
        ServiceAdmin,
        ServiceTypeAdmin,
        OrderAdmin,
        PaymentAdmin,
        SupportTicketAdmin,
        AdminUserAdmin,
    )

    admin_app.register_model(PlatformAdmin)
    admin_app.register_model(ServiceAdmin)
    admin_app.register_model(ServiceTypeAdmin)
    admin_app.register_model(OrderAdmin)
    admin_app.register_model(PaymentAdmin)
    admin_app.register_model(SupportTicketAdmin)
    admin_app.register_model(AdminUserAdmin)

    # Liens personnalisés
    admin_app.register_link(Link(label="Dashboard", icon="fas fa-tachometer-alt", url="/admin/dashboard"))
    admin_app.register_link(Link(label="Statistiques", icon="fas fa-chart-bar", url="/admin/stats"))

    return admin_app
