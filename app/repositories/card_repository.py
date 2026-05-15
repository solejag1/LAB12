"""Card repository with bank-specific queries."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.card import Card
from app.repositories.base_repository import BaseRepository


class CardRepository(BaseRepository[Card]):
    """Repository for Card model operations."""

    async def get_by_card_number(self, db: AsyncSession, card_number: str) -> Card | None:
        """Return a card by its 16-digit number."""
        result = await db.execute(select(Card).where(Card.card_number == card_number))
        return result.scalar_one_or_none()

    async def get_by_account(self, db: AsyncSession, account_id: int) -> list[Card]:
        """Return all cards linked to a specific account."""
        result = await db.execute(select(Card).where(Card.account_id == account_id))
        return list(result.scalars().all())

    async def get_active_by_account(self, db: AsyncSession, account_id: int) -> list[Card]:
        """Return non-blocked cards linked to a specific account."""
        result = await db.execute(
            select(Card).where(Card.account_id == account_id, Card.is_blocked.is_(False))
        )
        return list(result.scalars().all())


card_repository = CardRepository(Card)
