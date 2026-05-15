"""Tests for /api/v1/history endpoint and transaction recording."""
import pytest

from tests.conftest import get_auth_headers


@pytest.mark.asyncio
async def test_history_returns_transactions_for_own_account(client, test_user, test_account):
    resp = await client.get(
        f"/api/v1/history/{test_account.id}", headers=get_auth_headers(test_user)
    )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_history_for_foreign_account_returns_403(client, test_user2, test_account):
    resp = await client.get(
        f"/api/v1/history/{test_account.id}", headers=get_auth_headers(test_user2)
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_history_records_payment_transaction(client, test_user, test_account):
    await client.post(
        "/api/v1/payments/",
        json={"account_id": test_account.id, "amount": "200.00", "recipient": "Тест"},
        headers=get_auth_headers(test_user),
    )
    resp = await client.get(
        f"/api/v1/history/{test_account.id}", headers=get_auth_headers(test_user)
    )
    assert resp.status_code == 200
    types = [t["transaction_type"] for t in resp.json()]
    assert "payment" in types


@pytest.mark.asyncio
async def test_history_without_auth_returns_401(client, test_account):
    resp = await client.get(f"/api/v1/history/{test_account.id}")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_health_endpoint_returns_ok(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
