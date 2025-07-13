from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.admin import Admin
from schemas.admin import AdminCreate, AdminLogin, AdminResponse
from schemas.auth import Token
from utils.auth import authenticate_admin, create_access_token, get_password_hash, get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin Authentication"])

@router.post("/login", response_model=Token)
async def login_admin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    admin.last_login = datetime.utcnow()
    db.commit()
    
    access_token = create_access_token(data={"sub": admin.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=AdminResponse)
async def register_admin(
    admin: AdminCreate,
    db: Session = Depends(get_db),
    #current_admin: Admin = Depends(get_current_admin)
):
    # Check if admin already exists
    existing_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin with this email already exists")
    
    # Create new admin
    hashed_password = get_password_hash(admin.password)
    db_admin = Admin(
        email=admin.email,
        password_hash=hashed_password,
        role=admin.role
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

@router.get("/me", response_model=AdminResponse)
async def get_current_admin_info(
    current_admin: Admin = Depends(get_current_admin)
):
    return current_admin 