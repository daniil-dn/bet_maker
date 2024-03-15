from app.crud.base import CRUDBase
# app
from app.models import BetStatus
from app.schemas import crud_schemas


class CRUDBetStatus(
    CRUDBase[BetStatus,
    crud_schemas.BetStatusCreate,
    crud_schemas.BetStatusUpdate]
):
    pass


crud_bet_status = CRUDBetStatus(BetStatus)
