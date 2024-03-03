from http import HTTPStatus

import pytest
from httpx import AsyncClient

from zimplorer.main import PREFIX


@pytest.mark.asyncio
async def test_dummy_get(
    client: AsyncClient,
):
    response = await client.get(f"{PREFIX}/dummy")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert "value" in response_json
    assert response_json["value"] == "something"
