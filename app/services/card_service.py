"""Card issuance and management business logic."""
import random
import string

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.account_repository import account_repository
from app.repositories.card_repository import card_repository
from app.schemas.card import CardCreate


def _generate_card_number() -> str:
    """Generate a random 16-digit card number."""
    return "".join(random.choices(string.digits, k=16))


class CardService:
    """Handles card issuance, blocking, and deletion."""

    async def issue_card(self, db: AsyncSession, owner_id: int, data: CardCreate):
        """Issue a new card; verify the account belongs to the requesting user."""
        account = await account_repository.get(db, data.account_id)
        if account is None or not account.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        if account.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        while True:
            number = _generate_card_number()
            if not await card_repository.get_by_card_number(db, number):
                break

        return await card_repository.create(
            db,
            {
                "account_id": data.account_id,
                "card_number": number,
                "cardholder_name": data.cardholder_name,
                "expiry_date": data.expiry_date,
                "card_type": data.card_type,
                "is_blocked": False,
            },
        )

    async def get_card(self, db: AsyncSession, card_id: int, owner_id: int):
        """Return a card; raise 404/403 on missing or unauthorized access."""
        card = await card_repository.get(db, card_id)
        if card is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
        account = await account_repository.get(db, card.account_id)
        if account is None or account.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return card

    async def block_card(self, db: AsyncSession, card_id: int, owner_id: int):
        """Block an active card."""
        card = await self.get_card(db, card_id, owner_id)
        if card.is_blocked:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Card is already blocked")
        return await card_repository.update(db, card, {"is_blocked": True})

    async def unblock_card(self, db: AsyncSession, card_id: int, owner_id: int):
        """Unblock a previously blocked card."""
        card = await self.get_card(db, card_id, owner_id)
        if not card.is_blocked:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Card is not blocked"
            )
        return await card_repository.update(db, card, {"is_blocked": False})

    async def delete_card(self, db: AsyncSession, card_id: int, owner_id: int) -> bool:
        """Permanently delete a card."""
        card = await self.get_card(db, card_id, owner_id)
        return await card_repository.delete(db, card)


card_service = CardService()
