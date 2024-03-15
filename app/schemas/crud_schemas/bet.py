import decimal
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties

class BetInDB(BaseModel):
    id: int
    event_id: int
    status_id: int
    amount: decimal.Decimal
    updated_at: Optional[datetime] = None
    created_at: datetime


class BetCreate(BaseModel):
    event_id: int
    amount: decimal.Decimal
    status_id: int


class BetUpdate(BaseModel):
    id: int
    event_id: Optional[int] = None
    amount: Optional[decimal.Decimal] = None
    status_id: Optional[int] = None
