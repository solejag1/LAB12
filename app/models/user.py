"""User (bank client) SQLAlchemy model."""
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.account import Account


class User(Base, TimestampMixin):
    """Represents a bank client."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[str] = mapped_column(
        Enum("client", "admin", name="user_role"),
        default="client",
        nullable=False,
    )

    accounts: Mapped[list["Account"]] = relationship(
        "Account", back_populates="owner", lazy="selectin"
    )
