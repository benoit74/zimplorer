from http import HTTPStatus
from json import JSONDecodeError
from urllib.parse import urljoin

import requests
from fastapi import APIRouter

from zimplorer.constants import BackendConf, logger
from zimplorer.routes.schemas import BookSearchResult, SearchRequest

router = APIRouter(
    prefix="/books_search",
    tags=["all"],
)


@router.post(
    "",
    responses={
        200: {
            "description": "Returns a search result",
        },
    },
)
async def search_book(item: SearchRequest) -> BookSearchResult:
    request = SearchRequest.model_dump(item, exclude_none=True, by_alias=True)
    request["facets"] = [
        "project",
        "language",
        "selection",
        "flavour",
        "category",
        "size",
        "mediaCount",
        "articleCount",
        "creator",
        "publisher",
        "tags",
    ]
    response = requests.post(
        urljoin(
            BackendConf.meilisearch_url_safe,
            f"/indexes/{BackendConf.meilisearch_prod_index}/search",
        ),
        json=request,
        timeout=BackendConf.http_timeout,
    )
    if response.status_code >= HTTPStatus.BAD_REQUEST:
        logger.debug(f"HTTP {response.status_code}")
        if response.content:
            try:
                logger.debug(f"Meilisearch response: {response.json()}")
            except JSONDecodeError:
                logger.debug(
                    f"Meilisearch response: {response.content.decode('UTF-8')}"
                )
        response.raise_for_status()
    try:
        result = BookSearchResult.model_validate_json(response.content)
    except Exception as exc:
        logger.debug("Failed to serialize", exc_info=exc)
        raise
    return result
