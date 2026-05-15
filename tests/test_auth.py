"""Tests for /api/v1/auth endpoints."""
import pytest
from faker import Faker

fake = Faker("ru_RU")


def _reg(**overrides) -> dict:
    """Build a valid registration payload."""
    base = {
        "username": fake.unique.user_name()[:20],
        "email": fake.unique.email(),
        "password": "SecurePass1",
        "full_name": fake.name(),
    }
    base.update(overrides)
    return base


@pytest.mark.asyncio
async def test_register_with_valid_data_returns_201(client):
    resp = await client.post("/api/v1/auth/register", json=_reg())
    assert resp.status_code == 201
    body = resp.json()
    assert "id" in body
    assert "hashed_password" not in body
    assert body["role"] == "client"


@pytest.mark.asyncio
async def test_register_with_duplicate_username_returns_409(client):
    payload = _reg()
    await client.post("/api/v1/auth/register", json=payload)
    resp = await client.post("/api/v1/auth/register", json={**payload, "email": fake.unique.email()})
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_register_with_duplicate_email_returns_409(client):
    payload = _reg()
    await client.post("/api/v1/auth/register", json=payload)
    resp = await client.post(
        "/api/v1/auth/register", json={**payload, "username": fake.unique.user_name()[:20]}
    )
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_register_with_weak_password_no_digit_returns_422(client):
    resp = await client.post("/api/v1/auth/register", json=_reg(password="NoDigitPass"))
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_register_with_weak_password_no_letter_returns_422(client):
    resp = await client.post("/api/v1/auth/register", json=_reg(password="12345678"))
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_register_with_short_username_returns_422(client):
    resp = await client.post("/api/v1/auth/register", json=_reg(username="ab"))
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_login_with_valid_credentials_returns_token(client):
    payload = _reg()
    await client.post("/api/v1/auth/register", json=payload)
    resp = await client.post(
        "/api/v1/auth/login",
        data={"username": payload["username"], "password": payload["password"]},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_login_with_wrong_password_returns_401(client):
    payload = _reg()
    await client.post("/api/v1/auth/register", json=payload)
    resp = await client.post(
        "/api/v1/auth/login",
        data={"username": payload["username"], "password": "WrongPass9"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_with_nonexistent_user_returns_401(client):
    resp = await client.post(
        "/api/v1/auth/login", data={"username": "ghost_user", "password": "AnyPass1"}
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_me_with_valid_token_returns_user(client, test_user):
    from tests.conftest import get_auth_headers

    resp = await client.get("/api/v1/auth/me", headers=get_auth_headers(test_user))
    assert resp.status_code == 200
    assert resp.json()["username"] == test_user.username


@pytest.mark.asyncio
async def test_get_me_without_token_returns_401(client):
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_me_with_invalid_token_returns_401(client):
    resp = await client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid.jwt.token"})
    assert resp.status_code == 401
