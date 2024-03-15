import json
from datetime import datetime
from typing import Any, List

import aiohttp
import pytz
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import deps
from app.crud import crud_bet, crud_bet_status
from app.logs import server_log
from app.models import Bet, BetStatus
from app.schemas import api_schemas
from app.schemas import crud_schemas

# app

router = APIRouter()


@router.post("/bet", response_model=api_schemas.BetGetResponseAPI)
async def bet(
        message_in: api_schemas.BetCreateAPI,
        db: AsyncSession = Depends(deps.get_db),
) -> Any:
    # Получаем событие из сервиса провайдера
    async with aiohttp.ClientSession(trust_env=True) as session:
        url_get_event = f"http://app_line_provider:9090/api/v1/event/{message_in.event_id}"
        async with session.get(url_get_event) as response:
            content: bytes = await response.content.read()
            if response.status != 200:
                raise HTTPException(status_code=404, detail='Event not found')
    # Получаем данные собятия из ответа и валидируем
    event_dict: dict = json.loads(content.decode('utf-8'))
    event = api_schemas.EventGetAPI(**event_dict)
    server_log.debug(f'Get event for bet id:{event.id} status:{event.status_id}')
    # Проверяем статус и время дедлайна
    if event.status_id != 1 or event.deadline_dt < datetime.now(tz=pytz.UTC):
        raise HTTPException(status_code=400, detail='You cant bet on this event')
    bet_indb: Bet = await crud_bet.create(
        db,
        obj_in=crud_schemas.BetCreate(
            **message_in.model_dump(),
            status_id=1
        )
    )
    server_log.debug(f'Created bet id:{bet_indb.id} status:{bet_indb.status_id}')
    return api_schemas.BetGetResponseAPI(**bet_indb.__dict__, status='ещё не сыграла')


@router.get("/bets", response_model=List[api_schemas.BetGetResponseAPI])
async def bets(
        db: AsyncSession = Depends(deps.get_db),
) -> Any:
    # Получаем все статусы бетов
    bet_statuses_db: list[BetStatus] = await crud_bet_status.get_all(db)
    # Собираем имена статусов
    bet_statuses_dict: dict = {bet_status.id: bet_status.name for bet_status in bet_statuses_db}
    server_log.debug(f"Get all Bets len:{len(bet_statuses_db)} status names:{bet_statuses_dict}")
    return [
        api_schemas.BetGetResponseAPI(**bet.__dict__, status=bet_statuses_dict[bet.status_id])
        for bet in await crud_bet.get_all(db)]
