import asyncio
import json

import aio_pika

from app.core.config import settings
from app.crud import crud_bet
from app.db import SessionLocal
from app.logs import armq_bet_maker_log
from app.models import Bet
from app.schemas import crud_schemas
from app.schemas.armq_schemas import EventCallback


class Consumer:
    __slots__ = (
        'connection', 'channel',
    )

    async def run(self):
        armq_bet_maker_log.info(f'ARMQ_URL: {settings.ARMQ_URL}')
        # Creating connection
        self.connection = await aio_pika.connect_robust(
            settings.ARMQ_URL, timeout=80
        )
        # Creating channel
        self.channel = await self.connection.channel()

        # Declaring queue
        queue = await self.channel.declare_queue(
            'event_callback', durable=True, auto_delete=False
        )
        # Consuming
        await queue.consume(self.event_callback)

        try:
            # Wait until terminate
            await asyncio.Future()
        finally:
            await self.connection.close()

    async def event_callback(
            self,
            message: aio_pika.abc.AbstractIncomingMessage,
    ) -> None:
        # Process message
        async with message.process(requeue=True):
            # Получаем данные и валидируем поля
            data_dict: dict = json.loads(message.body)
            data = EventCallback(**data_dict)
            armq_bet_maker_log.info(f"Process Event Callback id:{data.id} status:{data.status_id}")
            async with SessionLocal() as db:
                bets_with_event: list[Bet] = await crud_bet.get_by_event_id(
                    db,
                    event_id=data.id
                )
                # Обновляем статус бетов
                for bet in bets_with_event:
                    bet_status = 1
                    if data.status_id == 2:
                        bet_status = 2
                    elif data.status_id == 3:
                        bet_status = 3
                    await crud_bet.update(
                        db,
                        db_obj=bet,
                        obj_in=crud_schemas.BetUpdate(
                            id=bet.id,
                            status_id=bet_status
                        )
                    )
