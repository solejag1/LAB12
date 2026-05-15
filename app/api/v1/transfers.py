"""Transfer and payment endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_active_user, get_db
from app.schemas.transfer import (
    PaymentCreate,
    PaymentResponse,
    TransferCreate,
    TransferResponse,
)
from app.services.transfer_service import transfer_service

transfers_router = APIRouter(prefix="/transfers", tags=["transfers"])
payments_router = APIRouter(prefix="/payments", tags=["payments"])


# ── Transfers ────────────────────────────────────────────────────────────────

@transfers_router.post("/", status_code=status.HTTP_201_CREATED)
async def make_transfer(
    data: TransferCreate,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Transfer money between two accounts."""
    return await transfer_service.transfer(db, current_user.id, data)


@transfers_router.get("/")
async def list_transfers(
    account_id: int,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Return all transfers for the specified account."""
    return await transfer_service.get_transfers(db, current_user.id, account_id)


# ── Payments ─────────────────────────────────────────────────────────────────

@payments_router.post("/", status_code=status.HTTP_201_CREATED)
async def make_payment(
    data: PaymentCreate,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Make a payment from an account."""
    return await transfer_service.make_payment(db, current_user.id, data)


@payments_router.get("/")
async def list_payments(
    account_id: int,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Return all payments for the specified account."""
    return await transfer_service.get_payments(db, current_user.id, account_id)
