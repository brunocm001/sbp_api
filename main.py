from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routers import (
    platforms_router,
    services_router,
    service_types_router,
    orders_router,
    payments_router,
    support_router,
    admin_router
)
from config import settings

# Import de l'admin
from admin.config import configure_admin
from admin.routes import router as admin_routes

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="API pour SocialBoost Pro - Services de boost sur les réseaux sociaux",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(admin_router)
app.include_router(platforms_router)
app.include_router(services_router)
app.include_router(service_types_router)
app.include_router(orders_router)
app.include_router(payments_router)
app.include_router(support_router)

# Include admin routes
app.include_router(admin_routes)

# Configure and mount admin app
admin_app = configure_admin()
app.mount("/admin", admin_app)

@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API SocialBoost Pro",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "admin": "/admin"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "SocialBoost Pro API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    ) 