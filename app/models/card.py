"""Bank card SQLAlchemy model."""
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.account import Account


class Card(Base, TimestampMixin):
    """Represents a bank card linked to an account."""

    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False, index=True)
    card_number: Mapped[str] = mapped_column(String(16), unique=True, index=True, nullable=False)
    cardholder_name: Mapped[str] = mapped_column(String(150), nullable=False)
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)
    card_type: Mapped[str] = mapped_column(
        Enum("debit", "credit", name="card_type"),
        default="debit",
        nullable=False,
    )
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    account: Mapped["Account"] = relationship("Account", back_populates="cards", lazy="selectin")
