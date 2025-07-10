from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.resources import Link
from fastapi_admin.models import AbstractAdmin
from fastapi_admin.file_upload import FileUpload
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine
from models import Admin
from utils.auth import verify_password
from typing import Optional

# Configuration de l'upload de fichiers
file_upload = FileUpload(uploads_dir="static/uploads")

# Provider d'authentification personnalisé
class CustomLoginProvider(UsernamePasswordProvider):
    async def authenticate(self, username: str, password: str) -> Optional[AbstractAdmin]:
        """Authentification personnalisée avec nos modèles Admin"""
        async with AsyncSession(engine) as session:
            admin = await session.get(Admin, username)
            if admin and verify_password(password, admin.password_hash):
                return admin
        return None

# Configuration de l'application admin
admin_app.configure(
    logo_url="https://preview.tabler.io/static/logo-white.svg",
    template_folders=["templates"],
    providers=[
        CustomLoginProvider(
            login_logo_url="https://preview.tabler.io/static/logo.svg",
            admin_model=Admin,
        )
    ],
    redis_url="redis://localhost:6379/0",
)

# Import des modèles admin
from .models import (
    PlatformAdmin,
    ServiceAdmin,
    ServiceTypeAdmin,
    OrderAdmin,
    PaymentAdmin,
    SupportTicketAdmin,
    AdminUserAdmin
)

# Enregistrement des modèles admin
admin_app.register_model(PlatformAdmin)
admin_app.register_model(ServiceAdmin)
admin_app.register_model(ServiceTypeAdmin)
admin_app.register_model(OrderAdmin)
admin_app.register_model(PaymentAdmin)
admin_app.register_model(SupportTicketAdmin)
admin_app.register_model(AdminUserAdmin)

# Liens personnalisés
admin_app.register_link(
    Link(
        label="Dashboard",
        icon="fas fa-tachometer-alt",
        url="/admin/dashboard",
    )
)

admin_app.register_link(
    Link(
        label="Statistiques",
        icon="fas fa-chart-bar",
        url="/admin/stats",
    )
) 