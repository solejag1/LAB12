"""Authentication endpoints: register, login, /me."""
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_active_user, get_db
from app.schemas.auth import Token, UserRegister, UserResponse
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    """Register a new bank client."""
    user = await auth_service.register(db, data)
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Authenticate and return a JWT access token."""
    user = await auth_service.authenticate(db, form_data.username, form_data.password)
    token = auth_service.create_token(user)
    return Token(access_token=token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_active_user)):
    """Return the profile of the authenticated user."""
    return current_user
