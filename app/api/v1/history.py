"""Transaction history endpoint."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_active_user, get_db
from app.repositories.transaction_repository import transaction_repository
from app.schemas.transaction import TransactionResponse
from app.services.account_service import account_service

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/{account_id}", response_model=list[TransactionResponse])
async def get_history(
    account_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Return paginated transaction history for the specified account."""
    await account_service.get_account(db, account_id, current_user.id)
    return await transaction_repository.get_by_account(db, account_id, skip=skip, limit=limit)
