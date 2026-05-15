"""Account request/response schemas."""
from decimal import Decimal
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    """Schema for opening a new bank account."""

    account_type: Literal["checking", "savings", "credit"] = "checking"
    currency: str = Field(default="RUB", max_length=3)
    initial_deposit: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)


class AccountUpdate(BaseModel):
    """Schema for updating account details."""

    currency: str | None = Field(default=None, max_length=3)


class AccountResponse(BaseModel):
    """Full account representation returned by the API."""

    model_config = {"from_attributes": True}

    id: int
    account_number: str
    account_type: str
    balance: Decimal
    currency: str
    is_active: bool
    owner_id: int
    created_at: datetime
