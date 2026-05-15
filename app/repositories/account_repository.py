"""Account repository with bank-specific queries."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.repositories.base_repository import BaseRepository


class AccountRepository(BaseRepository[Account]):
    """Repository for Account model operations."""

    async def get_by_account_number(self, db: AsyncSession, account_number: str) -> Account | None:
        """Return an account by its unique account number."""
        result = await db.execute(select(Account).where(Account.account_number == account_number))
        return result.scalar_one_or_none()

    async def get_by_owner(self, db: AsyncSession, owner_id: int) -> list[Account]:
        """Return all accounts belonging to a specific user."""
        result = await db.execute(
            select(Account).where(Account.owner_id == owner_id, Account.is_active.is_(True))
        )
        return list(result.scalars().all())

    async def get_active(self, db: AsyncSession) -> list[Account]:
        """Return all active accounts."""
        result = await db.execute(select(Account).where(Account.is_active.is_(True)))
        return list(result.scalars().all())


account_repository = AccountRepository(Account)
