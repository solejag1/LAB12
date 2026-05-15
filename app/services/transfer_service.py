"""Transfer and payment business logic."""
import uuid
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction
from app.repositories.account_repository import account_repository
from app.repositories.transaction_repository import transaction_repository
from app.schemas.transfer import PaymentCreate, TransferCreate


class TransferService:
    """Handles money transfers and payments between accounts."""

    async def _get_owned_account(self, db: AsyncSession, account_id: int, owner_id: int):
        """Return an active account that belongs to owner_id; raise otherwise."""
        account = await account_repository.get(db, account_id)
        if account is None or not account.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        if account.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return account

    async def transfer(
        self, db: AsyncSession, owner_id: int, data: TransferCreate
    ) -> dict:
        """Execute a transfer; debit source and credit destination atomically."""
        if data.from_account_id == data.to_account_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Source and destination accounts must be different",
            )

        from_account = await self._get_owned_account(db, data.from_account_id, owner_id)

        to_account = await account_repository.get(db, data.to_account_id)
        if to_account is None or not to_account.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Destination account not found"
            )

        if from_account.balance < data.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds"
            )

        ref = str(uuid.uuid4())[:8].upper()
        new_from_balance = from_account.balance - data.amount
        new_to_balance = to_account.balance + data.amount

        await account_repository.update(db, from_account, {"balance": new_from_balance})
        await account_repository.update(db, to_account, {"balance": new_to_balance})

        tx_out = await transaction_repository.create(
            db,
            {
                "account_id": from_account.id,
                "transaction_type": "transfer_out",
                "amount": data.amount,
                "balance_after": new_from_balance,
                "description": data.description or f"Transfer to account {to_account.account_number}",
                "reference_id": ref,
                "status": "completed",
            },
        )
        await transaction_repository.create(
            db,
            {
                "account_id": to_account.id,
                "transaction_type": "transfer_in",
                "amount": data.amount,
                "balance_after": new_to_balance,
                "description": data.description or f"Transfer from account {from_account.account_number}",
                "reference_id": ref,
                "status": "completed",
            },
        )

        return {
            "id": tx_out.id,
            "from_account_id": from_account.id,
            "to_account_id": to_account.id,
            "amount": data.amount,
            "status": "completed",
            "description": data.description,
            "created_at": tx_out.created_at,
        }

    async def get_transfers(self, db: AsyncSession, owner_id: int, account_id: int) -> list[Transaction]:
        """Return all transfer transactions for an owned account."""
        account = await self._get_owned_account(db, account_id, owner_id)
        result = []
        for tx_type in ("transfer_out", "transfer_in"):
            result.extend(await transaction_repository.get_by_type(db, account.id, tx_type))
        return sorted(result, key=lambda t: t.created_at, reverse=True)

    async def make_payment(
        self, db: AsyncSession, owner_id: int, data: PaymentCreate
    ) -> dict:
        """Deduct a payment from the specified account."""
        account = await self._get_owned_account(db, data.account_id, owner_id)

        if account.balance < data.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds"
            )

        ref = str(uuid.uuid4())[:8].upper()
        new_balance = account.balance - data.amount
        await account_repository.update(db, account, {"balance": new_balance})

        tx = await transaction_repository.create(
            db,
            {
                "account_id": account.id,
                "transaction_type": "payment",
                "amount": data.amount,
                "balance_after": new_balance,
                "description": data.description or f"Payment to {data.recipient}",
                "reference_id": ref,
                "status": "completed",
            },
        )

        return {
            "id": tx.id,
            "account_id": account.id,
            "amount": data.amount,
            "status": "completed",
            "description": tx.description,
            "created_at": tx.created_at,
        }

    async def get_payments(self, db: AsyncSession, owner_id: int, account_id: int) -> list[Transaction]:
        """Return all payment transactions for an owned account."""
        account = await self._get_owned_account(db, account_id, owner_id)
        return await transaction_repository.get_by_type(db, account.id, "payment")


transfer_service = TransferService()
