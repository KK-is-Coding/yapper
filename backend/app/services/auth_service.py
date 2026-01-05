from sqlmodel import Session, select
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.models.user import User
from app.schemas.auth import UserRegister, Token
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:
    @staticmethod
    def register_user(user_data: UserRegister, db: Session) -> dict:
        # Check if user exists
        existing_user = db.exec(
            select(User).where(User.username == user_data.username)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Create new user
        new_user = User(
            username=user_data.username,
            hashed_password=hash_password(user_data.password),
            created_at=datetime.now(timezone.utc).isoformat()
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User registered successfully", "username": new_user.username}

    @staticmethod
    def login_user(username: str, password: str, db: Session) -> Token:
        # Find user
        user = db.exec(
            select(User).where(User.username == username)
        ).first()

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        # Create token
        access_token = create_access_token(
            data={"sub": user.id, "username": user.username}
        )

        return Token(access_token=access_token, token_type="bearer")
