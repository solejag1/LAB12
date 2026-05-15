"""Transaction SQLAlchemy model — records every debit/credit operation."""
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.account import Account


class Transaction(Base, TimestampMixin):
    """Records every financial operation on an account."""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False, index=True)
    transaction_type: Mapped[str] = mapped_column(
        Enum("debit", "credit", "transfer_in", "transfer_out", "payment", name="transaction_type"),
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    balance_after: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reference_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("completed", "failed", "pending", name="transaction_status"),
        default="completed",
        nullable=False,
    )

    account: Mapped["Account"] = relationship("Account", back_populates="transactions", lazy="selectin")
