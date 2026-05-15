"""Account management endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_active_user, get_db
from app.repositories.account_repository import account_repository
from app.schemas.account import AccountCreate, AccountResponse, AccountUpdate
from app.services.account_service import account_service

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=list[AccountResponse])
async def list_accounts(
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Return all active accounts owned by the current user."""
    return await account_repository.get_by_owner(db, current_user.id)


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def open_account(
    data: AccountCreate,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Open a new bank account for the authenticated user."""
    return await account_service.open_account(db, current_user.id, data)


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: int,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Return a specific account owned by the current user."""
    return await account_service.get_account(db, account_id, current_user.id)


@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: int,
    data: AccountUpdate,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update account details."""
    return await account_service.update_account(db, account_id, current_user.id, data)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def close_account(
    account_id: int,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Soft-close an account (balance must be zero)."""
    await account_service.close_account(db, account_id, current_user.id)
