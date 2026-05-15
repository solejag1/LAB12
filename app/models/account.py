"""Bank account SQLAlchemy model."""
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.card import Card
    from app.models.transaction import Transaction
    from app.models.user import User


class Account(Base, TimestampMixin):
    """Represents a bank account belonging to a client."""

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    account_number: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    account_type: Mapped[str] = mapped_column(
        Enum("checking", "savings", "credit", name="account_type"),
        default="checking",
        nullable=False,
    )
    balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=Decimal("0.00"), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="RUB", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="accounts", lazy="selectin")
    cards: Mapped[list["Card"]] = relationship("Card", back_populates="account", lazy="selectin")
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="account", lazy="selectin"
    )
