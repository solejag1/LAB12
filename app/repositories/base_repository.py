"""Generic async CRUD repository."""
from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):  # noqa: UP046
    """Generic base repository providing async CRUD operations."""

    def __init__(self, model: type[ModelType]) -> None:
        self._model = model

    async def get(self, db: AsyncSession, record_id: int) -> ModelType | None:
        """Return a single record by primary key, or None."""
        result = await db.execute(select(self._model).where(self._model.id == record_id))  # type: ignore[attr-defined]
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """Return a paginated list of records."""
        result = await db.execute(select(self._model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, obj_in: dict[str, Any]) -> ModelType:
        """Create and persist a new record."""
        instance = self._model(**obj_in)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

    async def update(self, db: AsyncSession, instance: ModelType, updates: dict[str, Any]) -> ModelType:
        """Apply updates to an existing record and persist."""
        for field, value in updates.items():
            setattr(instance, field, value)
        await db.commit()
        await db.refresh(instance)
        return instance

    async def delete(self, db: AsyncSession, instance: ModelType) -> bool:
        """Delete a record; return True on success."""
        await db.delete(instance)
        await db.commit()
        return True
