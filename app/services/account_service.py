"""Account management business logic."""
import random
import string
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.account_repository import account_repository
from app.repositories.transaction_repository import transaction_repository
from app.schemas.account import AccountCreate, AccountUpdate


def _generate_account_number() -> str:
    """Generate a random 20-digit account number."""
    return "".join(random.choices(string.digits, k=20))


class AccountService:
    """Handles opening, updating, and closing bank accounts."""

    async def open_account(self, db: AsyncSession, owner_id: int, data: AccountCreate):
        """Open a new bank account for the given owner."""
        # ensure account number uniqueness
        while True:
            number = _generate_account_number()
            if not await account_repository.get_by_account_number(db, number):
                break

        account = await account_repository.create(
            db,
            {
                "owner_id": owner_id,
                "account_number": number,
                "account_type": data.account_type,
                "balance": data.initial_deposit,
                "currency": data.currency,
                "is_active": True,
            },
        )

        # record initial deposit as a transaction if amount > 0
        if data.initial_deposit > Decimal("0.00"):
            await transaction_repository.create(
                db,
                {
                    "account_id": account.id,
                    "transaction_type": "credit",
                    "amount": data.initial_deposit,
                    "balance_after": data.initial_deposit,
                    "description": "Initial deposit",
                    "status": "completed",
                },
            )

        return account

    async def get_account(self, db: AsyncSession, account_id: int, owner_id: int):
        """Return an account; raise 404 if not found, 403 if not owned by user."""
        account = await account_repository.get(db, account_id)
        if account is None or not account.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        if account.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return account

    async def update_account(
        self, db: AsyncSession, account_id: int, owner_id: int, data: AccountUpdate
    ):
        """Update mutable account fields."""
        account = await self.get_account(db, account_id, owner_id)
        updates = {k: v for k, v in data.model_dump().items() if v is not None}
        return await account_repository.update(db, account, updates)

    async def close_account(self, db: AsyncSession, account_id: int, owner_id: int) -> bool:
        """Soft-close an account by marking it inactive."""
        account = await self.get_account(db, account_id, owner_id)
        if account.balance > Decimal("0.00"):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot close account with positive balance",
            )
        await account_repository.update(db, account, {"is_active": False})
        return True


account_service = AccountService()
