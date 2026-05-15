"""Card request/response schemas."""
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


class CardCreate(BaseModel):
    """Schema for issuing a new card linked to an account."""

    account_id: int
    cardholder_name: str = Field(min_length=2, max_length=150)
    expiry_date: date
    card_type: Literal["debit", "credit"] = "debit"


class CardResponse(BaseModel):
    """Card representation returned by the API."""

    model_config = {"from_attributes": True}

    id: int
    account_id: int
    card_number: str
    cardholder_name: str
    expiry_date: date
    card_type: str
    is_blocked: bool
    created_at: datetime
