"""Authentication schemas."""
import re

from pydantic import BaseModel, EmailStr, field_validator


class UserRegister(BaseModel):
    """Schema for registering a new bank client."""

    username: str
    email: EmailStr
    password: str
    full_name: str
    phone: str | None = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Require at least one letter and one digit."""
        if not re.search(r"[A-Za-z]", v) or not re.search(r"\d", v):
            raise ValueError("Password must contain at least one letter and one digit")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    @field_validator("username")
    @classmethod
    def username_length(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return v


class UserLogin(BaseModel):
    """Schema for login request (used in docs only; actual login uses form-data)."""

    username: str
    password: str


class Token(BaseModel):
    """JWT access token response."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Public user profile — never includes hashed_password."""

    model_config = {"from_attributes": True}

    id: int
    username: str
    email: str
    full_name: str
    phone: str | None
    is_active: bool
    role: str
