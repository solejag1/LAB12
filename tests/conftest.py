"""Pytest fixtures for the banking application test suite."""
import os

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-only-32c")

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.dependencies import get_db
from app.core.security import create_access_token, hash_password
from app.main import app
from app.models.base import Base
from app.models.user import User
from app.models.account import Account


@pytest.fixture()
async def async_engine():
    """In-memory SQLite engine; tables created fresh for each test."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture()
async def async_session(async_engine):
    """Async session bound to the test engine."""
    factory = async_sessionmaker(async_engine, expire_on_commit=False)
    async with factory() as session:
        yield session


@pytest.fixture()
async def client(async_engine):
    """Async HTTP test client with DB override."""
    factory = async_sessionmaker(async_engine, expire_on_commit=False)

    async def override_get_db():
        async with factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


async def make_user(
    session: AsyncSession,
    username: str = "testuser",
    email: str = "test@example.com",
    password: str = "Password1",
    role: str = "client",
) -> User:
    """Helper: create and persist a User directly."""
    from app.repositories.user_repository import user_repository

    return await user_repository.create(
        session,
        {
            "username": username,
            "email": email,
            "hashed_password": hash_password(password),
            "full_name": "Test User",
            "phone": None,
            "role": role,
            "is_active": True,
        },
    )


@pytest.fixture()
async def test_user(async_session):
    return await make_user(async_session)


@pytest.fixture()
async def test_user2(async_session):
    return await make_user(async_session, username="user2", email="user2@example.com")


def get_auth_headers(user: User) -> dict[str, str]:
    """Return Bearer auth headers for the given user."""
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
async def test_account(async_session, test_user) -> Account:
    """A pre-created checking account with 10 000 RUB balance."""
    from app.repositories.account_repository import account_repository

    return await account_repository.create(
        async_session,
        {
            "owner_id": test_user.id,
            "account_number": "12345678901234567890",
            "account_type": "checking",
            "balance": "10000.00",
            "currency": "RUB",
            "is_active": True,
        },
    )


@pytest.fixture()
async def test_account2(async_session, test_user2) -> Account:
    """A second account for transfer tests."""
    from app.repositories.account_repository import account_repository

    return await account_repository.create(
        async_session,
        {
            "owner_id": test_user2.id,
            "account_number": "09876543210987654321",
            "account_type": "checking",
            "balance": "5000.00",
            "currency": "RUB",
            "is_active": True,
        },
    )
