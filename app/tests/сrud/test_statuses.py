import pytest

from app.crud import crud_bet_status
from app.db.session import SessionLocal


@pytest.mark.asyncio
async def test_bet_statuses(session: SessionLocal) -> None:
    async with session:
        bet_statuses = await crud_bet_status.get_all(session)
    assert len(bet_statuses) >= 3
    for status in bet_statuses:
        if status.id == 1:
            assert status.name_id == 'not_finished'
        elif status.id == 2:
            assert status.name_id == 'win'
        elif status.id == 3:
            assert status.name_id == 'lose'
