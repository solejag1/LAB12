"""User repository with bank-specific queries."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model operations."""

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        """Return a user by email address."""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        """Return a user by username."""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_active_clients(self, db: AsyncSession) -> list[User]:
        """Return all active client users."""
        result = await db.execute(
            select(User).where(User.is_active.is_(True), User.role == "client")
        )
        return list(result.scalars().all())


user_repository = UserRepository(User)
