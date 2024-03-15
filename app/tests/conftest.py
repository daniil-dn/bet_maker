import asyncio

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.logs import tests_log
from app.start_bet_maker import app


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def session():
    tests_log.info("CREATE DB")
    async with SessionLocal() as db:
        yield db
