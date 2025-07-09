from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:nUjgMltVbvvOCbKQJzKqckIWWqlOmyNW@postgres.railway.internal:5432/railway")
    database_url_test: str = os.getenv("DATABASE_URL_TEST", "postgresql://username:password@localhost:5432/socialboost_pro_test")
    
    # JWT Configuration
    secret_key: str = os.getenv("SECRET_KEY", "jgMltVbvvOCbKQJzKqckIWWqlOmyNW")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Application Configuration
    app_name: str = os.getenv("APP_NAME", "SocialBoost Pro")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    allowed_hosts: List[str] = os.getenv("ALLOWED_HOSTS", "['*']").replace("[", "").replace("]", "").replace("'", "").split(",")
    
    # Admin Default Credentials
    admin_email: str = os.getenv("ADMIN_EMAIL", "admin@socialboostpro.com")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "admin123")

    class Config:
        env_file = ".env"

settings = Settings() 