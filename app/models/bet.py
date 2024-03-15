from datetime import datetime

from sqlalchemy import Column, DateTime, BigInteger, ForeignKey, Float

from app.db.base_class import Base
from app.models.model_base import ModelBase


class Bet(Base, ModelBase):
    id = Column(BigInteger, primary_key=True, index=True)
    event_id = Column(BigInteger, index=True, nullable=False)
    status_id = Column(BigInteger, ForeignKey("bet_status.id"), nullable=False)
    amount = Column(
        Float, nullable=False
    )  # коэффициент ставки на выигрыш — строго положительное число с двумя знаками после запятой,
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
