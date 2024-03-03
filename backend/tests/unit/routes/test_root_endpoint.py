from http import HTTPStatus

import pytest
from httpx import AsyncClient

from zimplorer.main import PREFIX


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get("", follow_redirects=False)
    assert response.status_code == HTTPStatus.TEMPORARY_REDIRECT
    response = await client.get("/", follow_redirects=False)
    assert response.status_code == HTTPStatus.TEMPORARY_REDIRECT
    response = await client.get("/", follow_redirects=True)
    assert str(response.url).endswith("/api" + PREFIX + "/")
    assert response.headers.get("Content-Type") == "text/html; charset=utf-8"
    assert "Swagger UI" in response.text
