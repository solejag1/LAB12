"""Tests for /api/v1/accounts endpoints."""
import pytest

from tests.conftest import get_auth_headers


@pytest.mark.asyncio
async def test_list_accounts_returns_own_accounts(client, test_user, test_account):
    resp = await client.get("/api/v1/accounts/", headers=get_auth_headers(test_user))
    assert resp.status_code == 200
    ids = [a["id"] for a in resp.json()]
    assert test_account.id in ids


@pytest.mark.asyncio
async def test_open_account_returns_201(client, test_user):
    resp = await client.post(
        "/api/v1/accounts/",
        json={"account_type": "savings", "currency": "RUB", "initial_deposit": "1000.00"},
        headers=get_auth_headers(test_user),
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["account_type"] == "savings"
    assert len(body["account_number"]) == 20


@pytest.mark.asyncio
async def test_open_account_with_initial_deposit_sets_balance(client, test_user):
    resp = await client.post(
        "/api/v1/accounts/",
        json={"account_type": "checking", "initial_deposit": "5000.00"},
        headers=get_auth_headers(test_user),
    )
    assert resp.status_code == 201
    assert float(resp.json()["balance"]) == 5000.0


@pytest.mark.asyncio
async def test_get_account_by_id_returns_account(client, test_user, test_account):
    resp = await client.get(
        f"/api/v1/accounts/{test_account.id}", headers=get_auth_headers(test_user)
    )
    assert resp.status_code == 200
    assert resp.json()["id"] == test_account.id


@pytest.mark.asyncio
async def test_get_account_with_nonexistent_id_returns_404(client, test_user):
    resp = await client.get("/api/v1/accounts/99999", headers=get_auth_headers(test_user))
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_account_owned_by_other_user_returns_403(client, test_user2, test_account):
    resp = await client.get(
        f"/api/v1/accounts/{test_account.id}", headers=get_auth_headers(test_user2)
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_update_account_currency(client, test_user, test_account):
    resp = await client.put(
        f"/api/v1/accounts/{test_account.id}",
        json={"currency": "USD"},
        headers=get_auth_headers(test_user),
    )
    assert resp.status_code == 200
    assert resp.json()["currency"] == "USD"


@pytest.mark.asyncio
async def test_close_account_with_zero_balance_returns_204(client, test_user):
    # Open a fresh account with zero balance
    create_resp = await client.post(
        "/api/v1/accounts/",
        json={"account_type": "checking", "initial_deposit": "0.00"},
        headers=get_auth_headers(test_user),
    )
    account_id = create_resp.json()["id"]
    resp = await client.delete(
        f"/api/v1/accounts/{account_id}", headers=get_auth_headers(test_user)
    )
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_close_account_with_positive_balance_returns_409(client, test_user, test_account):
    resp = await client.delete(
        f"/api/v1/accounts/{test_account.id}", headers=get_auth_headers(test_user)
    )
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_open_account_without_auth_returns_401(client):
    resp = await client.post("/api/v1/accounts/", json={"account_type": "checking"})
    assert resp.status_code == 401
