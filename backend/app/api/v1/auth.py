from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.api.deps import get_db
from app.schemas.auth import UserRegister, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=201)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    return AuthService.register_user(user_data, db)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    return AuthService.login_user(form_data.username, form_data.password, db)
