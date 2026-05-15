"""
Задание 3. Рефакторинг bad_commission.py — чистая версия.
Все проблемы устранены: type hints, async I/O, ORM, именованные константы, SRP.
"""
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Final

import httpx
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account

# ── Именованные константы вместо магических чисел ────────────────────────────
BASE_COMMISSION_RATE: Final[Decimal] = Decimal("0.03")
PROMO_DISCOUNTS: Final[dict[str, Decimal]] = {
    "PROMO10": Decimal("0.10"),
    "PROMO15": Decimal("0.15"),
    "VIP": Decimal("0.15"),
}
ACCOUNT_TYPE_DISCOUNT: Final[Decimal] = Decimal("0.05")
HIGH_AMOUNT_SURCHARGE: Final[Decimal] = Decimal("500.00")
MID_AMOUNT_SURCHARGE: Final[Decimal] = Decimal("100.00")
HIGH_AMOUNT_THRESHOLD: Final[Decimal] = Decimal("1000000.00")
MID_AMOUNT_THRESHOLD: Final[Decimal] = Decimal("500000.00")
COMMISSION_SERVICE_URL: Final[str] = "http://commission-service/api/verify"


@dataclass(frozen=True)
class CommissionResult:
    """Immutable result of commission calculation."""

    base_commission: Decimal
    discount_applied: Decimal
    surcharge: Decimal
    final_commission: Decimal
    promo_code: str | None


async def _get_account(db: AsyncSession, account_id: int) -> Account:
    """Fetch account from DB; raise 404 if not found."""
    result = await db.execute(select(Account).where(Account.id == account_id))
    account = result.scalar_one_or_none()
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


def _calculate_base_commission(amount: Decimal) -> Decimal:
    """Return the flat percentage commission."""
    return (amount * BASE_COMMISSION_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _apply_promo_discount(commission: Decimal, promo_code: str | None) -> tuple[Decimal, Decimal]:
    """Return (discounted_commission, discount_amount)."""
    if promo_code and promo_code in PROMO_DISCOUNTS:
        discount = (commission * PROMO_DISCOUNTS[promo_code]).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        return commission - discount, discount
    return commission, Decimal("0.00")


def _apply_account_type_discount(commission: Decimal, account_type: str) -> tuple[Decimal, Decimal]:
    """Apply a 5% discount for savings and credit accounts."""
    if account_type in ("savings", "credit"):
        discount = (commission * ACCOUNT_TYPE_DISCOUNT).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        return commission - discount, discount
    return commission, Decimal("0.00")


def _calculate_surcharge(amount: Decimal) -> Decimal:
    """Apply surcharges for large transfer amounts."""
    if amount > HIGH_AMOUNT_THRESHOLD:
        return HIGH_AMOUNT_SURCHARGE
    if amount > MID_AMOUNT_THRESHOLD:
        return MID_AMOUNT_SURCHARGE
    return Decimal("0.00")


async def calculate_commission(
    db: AsyncSession,
    account_id: int,
    amount: Decimal,
    promo_code: str | None = None,
) -> CommissionResult:
    """
    Calculate the transfer commission for a given account and amount.

    Args:
        db: Async database session.
        account_id: ID of the source account.
        amount: Transfer amount (must be positive).
        promo_code: Optional promotional discount code.

    Returns:
        CommissionResult with a breakdown of all charges.
    """
    if amount <= Decimal("0.00"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be positive"
        )

    account = await _get_account(db, account_id)

    base = _calculate_base_commission(amount)
    after_promo, promo_discount = _apply_promo_discount(base, promo_code)
    after_type, type_discount = _apply_account_type_discount(after_promo, account.account_type)
    surcharge = _calculate_surcharge(amount)

    total_discount = promo_discount + type_discount
    final = after_type + surcharge

    # Verify with external service using async HTTP client (non-blocking)
    try:
        async with httpx.AsyncClient(timeout=5.0) as http:
            await http.get(
                COMMISSION_SERVICE_URL,
                params={"amount": str(amount), "code": promo_code or ""},
            )
    except httpx.RequestError:
        # External verification is best-effort; do not fail the transaction
        pass

    return CommissionResult(
        base_commission=base,
        discount_applied=total_discount,
        surcharge=surcharge,
        final_commission=final,
        promo_code=promo_code,
    )
