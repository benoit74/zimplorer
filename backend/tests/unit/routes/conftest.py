from collections.abc import AsyncGenerator
from typing import Any

import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from zimplorer.main import Main


@pytest_asyncio.fixture()  # pyright: ignore
def app():
    return Main().create_app()


@pytest_asyncio.fixture()  # pyright: ignore
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(app=app, base_url="http://test/api") as client:
        yield client
