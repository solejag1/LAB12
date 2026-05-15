"""Transfer and payment schemas."""
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class TransferCreate(BaseModel):
    """Schema for initiating a money transfer between two accounts."""

    from_account_id: int
    to_account_id: int
    amount: Decimal = Field(gt=0, decimal_places=2)
    description: str | None = Field(default=None, max_length=255)


class TransferResponse(BaseModel):
    """Transfer result returned by the API."""

    model_config = {"from_attributes": True}

    id: int
    from_account_id: int
    to_account_id: int
    amount: Decimal
    status: str
    description: str | None
    created_at: datetime


class PaymentCreate(BaseModel):
    """Schema for making a payment from an account."""

    account_id: int
    amount: Decimal = Field(gt=0, decimal_places=2)
    recipient: str = Field(min_length=2, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class PaymentResponse(BaseModel):
    """Payment result returned by the API."""

    model_config = {"from_attributes": True}

    id: int
    account_id: int
    amount: Decimal
    status: str
    description: str | None
    created_at: datetime
