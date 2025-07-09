from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Include routers
app.include_router(admin_router)
app.include_router(platforms_router)
app.include_router(services_router)
app.include_router(service_types_router)
app.include_router(orders_router)
app.include_router(payments_router)
app.include_router(support_router)

@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API SocialBoost Pro",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
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