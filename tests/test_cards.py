"""Tests for /api/v1/cards endpoints."""
from datetime import date, timedelta

import pytest

from tests.conftest import get_auth_headers


def _card_payload(account_id: int, **overrides) -> dict:
    base = {
        "account_id": account_id,
        "cardholder_name": "Кучеров Олег",
        "expiry_date": str(date.today() + timedelta(days=365 * 3)),
        "card_type": "debit",
    }
    base.update(overrides)
    return base


@pytest.mark.asyncio
async def test_issue_card_returns_201(client, test_user, test_account):
    resp = await client.post(
        "/api/v1/cards/",
        json=_card_payload(test_account.id),
        headers=get_auth_headers(test_user),
    )
    assert resp.status_code == 201
    body = resp.json()
    assert len(body["card_number"]) == 16
    assert body["is_blocked"] is False


@pytest.mark.asyncio
async def test_issue_card_for_foreign_account_returns_403(client, test_user2, test_account):
    resp = await client.post(
        "/api/v1/cards/",
        json=_card_payload(test_account.id),
        headers=get_auth_headers(test_user2),
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_issue_card_for_nonexistent_account_returns_404(client, test_user):
    resp = await client.post(
        "/api/v1/cards/",
        json=_card_payload(99999),
        headers=get_auth_headers(test_user),
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_card_returns_card(client, test_user, test_account):
    create = await client.post(
        "/api/v1/cards/", json=_card_payload(test_account.id), headers=get_auth_headers(test_user)
    )
    card_id = create.json()["id"]
    resp = await client.get(f"/api/v1/cards/{card_id}", headers=get_auth_headers(test_user))
    assert resp.status_code == 200
    assert resp.json()["id"] == card_id


@pytest.mark.asyncio
async def test_block_card_changes_status(client, test_user, test_account):
    create = await client.post(
        "/api/v1/cards/", json=_card_payload(test_account.id), headers=get_auth_headers(test_user)
    )
    card_id = create.json()["id"]
    resp = await client.patch(f"/api/v1/cards/{card_id}/block", headers=get_auth_headers(test_user))
    assert resp.status_code == 200
    assert resp.json()["is_blocked"] is True


@pytest.mark.asyncio
async def test_block_already_blocked_card_returns_409(client, test_user, test_account):
    create = await client.post(
        "/api/v1/cards/", json=_card_payload(test_account.id), headers=get_auth_headers(test_user)
    )
    card_id = create.json()["id"]
    await client.patch(f"/api/v1/cards/{card_id}/block", headers=get_auth_headers(test_user))
    resp = await client.patch(f"/api/v1/cards/{card_id}/block", headers=get_auth_headers(test_user))
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_unblock_card_restores_active_status(client, test_user, test_account):
    create = await client.post(
        "/api/v1/cards/", json=_card_payload(test_account.id), headers=get_auth_headers(test_user)
    )
    card_id = create.json()["id"]
    await client.patch(f"/api/v1/cards/{card_id}/block", headers=get_auth_headers(test_user))
    resp = await client.patch(f"/api/v1/cards/{card_id}/unblock", headers=get_auth_headers(test_user))
    assert resp.status_code == 200
    assert resp.json()["is_blocked"] is False


@pytest.mark.asyncio
async def test_delete_card_returns_204(client, test_user, test_account):
    create = await client.post(
        "/api/v1/cards/", json=_card_payload(test_account.id), headers=get_auth_headers(test_user)
    )
    card_id = create.json()["id"]
    resp = await client.delete(f"/api/v1/cards/{card_id}", headers=get_auth_headers(test_user))
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_get_nonexistent_card_returns_404(client, test_user):
    resp = await client.get("/api/v1/cards/99999", headers=get_auth_headers(test_user))
    assert resp.status_code == 404
