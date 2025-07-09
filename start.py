#!/usr/bin/env python3
"""
Script de démarrage pour SocialBoost Pro
"""
import uvicorn
from config import settings

if __name__ == "__main__":
    print("🚀 Démarrage de SocialBoost Pro...")
    print(f"📊 Mode debug: {settings.debug}")
    print(f"🌐 URL: http://localhost:8000")
    print(f"📚 Documentation: http://localhost:8000/docs")
    print(f"🔧 ReDoc: http://localhost:8000/redoc")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    ) 