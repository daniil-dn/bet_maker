from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BetStatusInDB(BaseModel):
    id: int
    name_id: Optional[str]
    name: Optional[str]
    created_at: datetime


class BetStatusCreate(BaseModel):
    id: int
    name_id: str
    name: str


class BetStatusUpdate(BaseModel):
    pass
