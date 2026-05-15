"""Authentication and registration business logic."""
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import user_repository
from app.schemas.auth import UserRegister


class AuthService:
    """Handles user registration, login and token creation."""

    async def register(self, db: AsyncSession, data: UserRegister):
        """Register a new bank client; raise 409 on duplicate username/email."""
        if await user_repository.get_by_username(db, data.username):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
        if await user_repository.get_by_email(db, data.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        return await user_repository.create(
            db,
            {
                "username": data.username,
                "email": data.email,
                "hashed_password": hash_password(data.password),
                "full_name": data.full_name,
                "phone": data.phone,
                "role": "client",
                "is_active": True,
            },
        )

    async def authenticate(self, db: AsyncSession, username: str, password: str):
        """Return the user if credentials are valid; raise 401 otherwise."""
        user = await user_repository.get_by_username(db, username)
        if user is None or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
            )
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled")
        return user

    def create_token(self, user) -> str:
        """Create a JWT access token for a user."""
        return create_access_token({"sub": user.username, "role": user.role})


auth_service = AuthService()
