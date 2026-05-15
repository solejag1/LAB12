"""Seed the database with test data (idempotent)."""
import asyncio
import os

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/bank_db")

from decimal import Decimal

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.security import hash_password
from app.models.base import Base
from app.models.user import User
from app.models.account import Account

fake = Faker("ru_RU")


async def seed() -> None:
    engine = create_async_engine(settings.DATABASE_URL)
    factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with factory() as db:
        await _seed_users(db)

    await engine.dispose()
    print("✅ Seed completed.")


async def _seed_users(db: AsyncSession) -> None:
    from sqlalchemy import select

    existing = (await db.execute(select(User).where(User.username == "admin"))).scalar_one_or_none()
    if existing:
        print("ℹ️  Data already seeded, skipping.")
        return

    # Admin
    admin = User(
        username="admin",
        email="admin@bank.ru",
        hashed_password=hash_password("Admin123"),
        full_name="Администратор",
        role="admin",
        is_active=True,
    )
    db.add(admin)

    # 5 test clients with accounts
    for i in range(5):
        user = User(
            username=fake.unique.user_name()[:20],
            email=fake.unique.email(),
            hashed_password=hash_password("Client123"),
            full_name=fake.name(),
            phone=fake.phone_number()[:20],
            role="client",
            is_active=True,
        )
        db.add(user)
        await db.flush()

        account = Account(
            owner_id=user.id,
            account_number="".join([str(fake.random_digit()) for _ in range(20)]),
            account_type=fake.random_element(["checking", "savings"]),
            balance=Decimal(str(fake.random_int(min=1000, max=100000))),
            currency="RUB",
            is_active=True,
        )
        db.add(account)

    await db.commit()
    print("✅ Created admin + 5 clients with accounts.")


if __name__ == "__main__":
    asyncio.run(seed())
