from datetime import datetime

from sqlalchemy import Column, String, DateTime, BigInteger

from app.db.base_class import Base
from app.models.model_base import ModelBase


class BetStatus(Base, ModelBase):
    id = Column(BigInteger, primary_key=True, index=True)
    name_id = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
