"""Card management endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_active_user, get_db
from app.repositories.card_repository import card_repository
from app.schemas.card import CardCreate, CardResponse
from app.services.card_service import card_service

router = APIRouter(prefix="/cards", tags=["cards"])


@router.get("/", response_model=list[CardResponse])
async def list_cards(
    account_id: int | None = None,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Return cards for the current user's accounts; optionally filter by account_id."""
    if account_id:
        return await card_repository.get_by_account(db, account_id)
    # Return all cards across all user accounts
    from app.repositories.account_repository import account_repository as ar

    accounts = await ar.get_by_owner(db, current_user.id)
    cards = []
    for acc in accounts:
        cards.extend(await card_repository.get_by_account(db, acc.id))
    return cards


@router.post("/", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
async def issue_card(
    data: CardCreate,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Issue a new card linked to one of the user's accounts."""
    return await card_service.issue_card(db, current_user.id, data)


@router.get("/{card_id}", response_model=CardResponse)
async def get_card(
    card_id: int,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Return details of a specific card."""
    return await card_service.get_card(db, card_id, current_user.id)


@router.patch("/{card_id}/block", response_model=CardResponse)
async def block_card(
    card_id: int,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Block a card to prevent further transactions."""
    return await card_service.block_card(db, card_id, current_user.id)


@router.patch("/{card_id}/unblock", response_model=CardResponse)
async def unblock_card(
    card_id: int,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Unblock a previously blocked card."""
    return await card_service.unblock_card(db, card_id, current_user.id)


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(
    card_id: int,
    current_user=Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Permanently delete a card."""
    await card_service.delete_card(db, card_id, current_user.id)
