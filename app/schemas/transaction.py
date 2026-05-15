"""Transaction history schema."""
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class TransactionResponse(BaseModel):
    """A single transaction entry in the account history."""

    model_config = {"from_attributes": True}

    id: int
    account_id: int
    transaction_type: str
    amount: Decimal
    balance_after: Decimal
    description: str | None
    reference_id: str | None
    status: str
    created_at: datetime
