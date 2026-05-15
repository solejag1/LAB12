"""Transaction repository with bank-specific queries."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction
from app.repositories.base_repository import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    """Repository for Transaction model operations."""

    async def get_by_account(
        self, db: AsyncSession, account_id: int, skip: int = 0, limit: int = 50
    ) -> list[Transaction]:
        """Return paginated transactions for a given account, newest first."""
        result = await db.execute(
            select(Transaction)
            .where(Transaction.account_id == account_id)
            .order_by(Transaction.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_type(self, db: AsyncSession, account_id: int, tx_type: str) -> list[Transaction]:
        """Return transactions of a specific type for an account."""
        result = await db.execute(
            select(Transaction).where(
                Transaction.account_id == account_id,
                Transaction.transaction_type == tx_type,
            )
        )
        return list(result.scalars().all())


transaction_repository = TransactionRepository(Transaction)
