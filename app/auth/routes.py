from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.database import engine
from app.models import User
from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(username: str, password: str):
    with Session(engine) as session:
        existing = session.exec(
            select(User).where(User.username == username)
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

        user = User(
            username=username,
            hashed_password=hash_password(password)
        )

        session.add(user)
        session.commit()
        session.refresh(user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.username == form_data.username)
        ).first()

        if not user or not verify_password(
            form_data.password,
            user.hashed_password
        ):
            raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.id})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
