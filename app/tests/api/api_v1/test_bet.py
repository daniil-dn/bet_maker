from datetime import datetime, timedelta

import pytz
import requests
from httpx import AsyncClient
from mock import patch

from app.api.api_v1.endpoints.bet import bets
from app.core import settings
from app.models import Bet, BetStatus
from app.start_bet_maker import app

base_url = "http://localhost:9090"
line_provider_base_url = "http://app_line_provider:9090"


class TestEvent:

    async def test_create_bet(self) -> None:
        async with AsyncClient(app=app, base_url=base_url) as client:
            r = await client.get(
                f"{settings.API_V1_STR}/events"
            )
            assert r.status_code == 200
            events = r.json()
            if not events:
                data = {"coefficient": 1.22,
                        "deadline_ts": (datetime.now(tz=pytz.UTC) + timedelta(seconds=30)).timestamp()}

                r = requests.put(line_provider_base_url + "/api/v1/event", json=data)
                assert r.status_code == 200
                event = r.json()
            else:
                event = events[0]
            bet_data = {"event_id": event['id'], "amount": 1.22}
            r = await client.post(
                f"{settings.API_V1_STR}/bet",
                json=bet_data
            )
            assert r.status_code == 200

    async def test_get_bets(self) -> None:
        async with AsyncClient(app=app, base_url=base_url) as client:
            r = await client.get(
                f"{settings.API_V1_STR}/bets"
            )
            assert r.status_code == 200

    async def test_get_bets_mock(self) -> None:

        with patch('app.crud.crud_bet.get_all') as perm_mock_bet, patch(
                'app.crud.crud_bet_status.get_all'
        ) as perm_mock_bet_statuses:
            perm_mock_bet.return_value = [
                Bet(id=1, event_id=1, status_id=1, amount=1, updated_at=datetime.now(), created_at=datetime.now()),
                Bet(id=1, event_id=1, status_id=1, amount=1, updated_at=datetime.now(), created_at=datetime.now()),
                Bet(id=1, event_id=1, status_id=1, amount=1, updated_at=datetime.now(), created_at=datetime.now()),
                Bet(id=1, event_id=1, status_id=1, amount=1, updated_at=datetime.now(), created_at=datetime.now())
            ]
            perm_mock_bet_statuses.return_value = [
                BetStatus(id=1, name='ещё не сыграла', created_at=datetime.now()),
                BetStatus(id=2, name='Выиграла', created_at=datetime.now()),
                BetStatus(id=3, name='Проиграла', created_at=datetime.now())]
            test_bets = await bets()
            print(test_bets)
            assert len(test_bets) == 4

    async def test_get_events(self) -> None:
        async with AsyncClient(app=app, base_url=base_url) as client:
            r = await client.get(
                f"{settings.API_V1_STR}/events"
            )
            assert r.status_code == 200
