"""Tests for /api/v1/transfers and /api/v1/payments endpoints."""
import pytest

from tests.conftest import get_auth_headers, make_user


@pytest.mark.asyncio
async def test_transfer_deducts_from_source(client, test_user, test_account, async_session):
    """After a transfer, the source account balance should decrease."""
    user2 = await make_user(async_session, username="recv1", email="recv1@test.com")
    from app.repositories.account_repository import account_repository

    acc2 = await account_repository.create(
        async_session,
        {
            "owner_id": user2.id,
            "account_number": "11111111111111111111",
            "account_type": "checking",
            "balance": "0.00",
            "currency": "RUB",
            "is_active": True,
        },
    )

    resp = await client.post(
        "/api/v1/transfers/",
        json={
            "from_account_id": test_account.id,
            "to_account_id": acc2.id,
            "amount": "3000.00",
            "description": "Test transfer",
        },
        headers=get_auth_headers(test_user),
    )
    assert resp.status_code == 201
    assert float(resp.json()["amount"]) == 3000.0

    acc_resp = await client.get(
        f"/api/v1/accounts/{test_account.id}", headers=get_auth_headers(test_user)
    )
    assert float(acc_resp.json()["balance"]) == 7000.0


@pytest.mark.asyncio
async def test_transfer_with_insufficient_funds_returns_400(client, test_user, test_account, async_session):
    user2 = await make_user(async_session, username="recv2", email="recv2@test.com")
    from app.repositories.account_repository import account_repository

    acc2 = await account_repository.create(
        async_session,
        {
            "owner_id": user2.id,
            "account_number": "22222222222222222222",
            "account_type": "checking",
            "balance": "0.00",
            "currency": "RUB",
            "is_active": True,
        },
    )
    resp = await client.post(
        "/api/v1/transfers/",
        json={"from_account_id": test_account.id, "to_account_id": acc2.id, "amount": "999999.00"},
        headers=get_auth_headers(test_user),
    )
    assert resp.status_code == 400
    assert "Insufficient" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_transfer_to_same_account_returns_400(client, test_user, test_account):
    resp = await client.post(
        "/api/v1/transfers/",
        json={
            "from_account_id": test_account.id,
            "to_account_id": test_account.id,
            "amount": "100.00",
        },
        headers=get_auth_headers(test_user),
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_transfer_to_nonexistent_account_returns_404(client, test_user, test_account):
    resp = await client.post(
        "/api/v1/transfers/",
        json={"from_account_id": test_account.id, "to_account_id": 99999, "amount": "100.00"},
        headers=get_auth_headers(test_user),
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_transfer_from_foreign_account_returns_403(client, test_user2, test_account, async_session):
    """user2 tries to transfer FROM test_account that belongs to test_user → 403."""
    user3 = await make_user(async_session, username="recv3", email="recv3@test.com")
    from app.repositories.account_repository import account_repository

    acc3 = await account_repository.create(
        async_session,
        {
            "owner_id": user3.id,
            "account_number": "33333333333333333333",
            "account_type": "checking",
            "balance": "0.00",
            "currency": "RUB",
            "is_active": True,
        },
    )
    resp = await client.post(
        "/api/v1/transfers/",
        json={"from_account_id": test_account.id, "to_account_id": acc3.id, "amount": "100.00"},
        headers=get_auth_headers(test_user2),
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_payment_deducts_balance(client, test_user, test_account):
    resp = await client.post(
        "/api/v1/payments/",
        json={
            "account_id": test_account.id,
            "amount": "500.00",
            "recipient": "ПАО Ромашка",
            "description": "Оплата услуг",
        },
        headers=get_auth_headers(test_user),
    )
    assert resp.status_code == 201
    assert float(resp.json()["amount"]) == 500.0

    acc_resp = await client.get(
        f"/api/v1/accounts/{test_account.id}", headers=get_auth_headers(test_user)
    )
    assert float(acc_resp.json()["balance"]) == 9500.0


@pytest.mark.asyncio
async def test_payment_with_insufficient_funds_returns_400(client, test_user, test_account):
    resp = await client.post(
        "/api/v1/payments/",
        json={"account_id": test_account.id, "amount": "99999.00", "recipient": "Кто-то"},
        headers=get_auth_headers(test_user),
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_payment_with_zero_amount_returns_422(client, test_user, test_account):
    resp = await client.post(
        "/api/v1/payments/",
        json={"account_id": test_account.id, "amount": "0.00", "recipient": "Test"},
        headers=get_auth_headers(test_user),
    )
    assert resp.status_code == 422
