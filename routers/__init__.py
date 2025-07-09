from .platforms import router as platforms_router
from .services import router as services_router
from .service_types import router as service_types_router
from .orders import router as orders_router
from .payments import router as payments_router
from .support import router as support_router
from .admin import router as admin_router

__all__ = [
    "platforms_router",
    "services_router", 
    "service_types_router",
    "orders_router",
    "payments_router",
    "support_router",
    "admin_router"
] 