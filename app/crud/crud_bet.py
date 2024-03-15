from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
# app
from app.models import Bet
from app.schemas import crud_schemas


class CRUDBet(
    CRUDBase[Bet,
    crud_schemas.BetCreate,
    crud_schemas.BetUpdate]
):
    async def get_all_not_processed(
            self, db: AsyncSession
    ) -> List[Bet]:
        q = select(Bet).filter(Bet.status_id == 1)
        res = await db.execute(q)
        return res.scalars().all()

    async def get_by_event_id(
            self, db: AsyncSession, *, event_id: int
    ) -> List[Bet]:
        q = select(Bet).filter(Bet.event_id == event_id)
        res = await db.execute(q)
        return res.scalars().all()


crud_bet = CRUDBet(Bet)
