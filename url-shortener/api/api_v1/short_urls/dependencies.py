import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
    Query,
)
from starlette import status

from core.config import API_TOKENS
from schemas.short_url import ShortUrl

from .crud import storage


log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)


def prefetch_short_urls(
    slug: str,
) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)

    if url:
        return url

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


def save_storage_state(
    background_tasks: BackgroundTasks,
    request: Request,
):
    # сначала выполняется код до входа в view
    yield
    # код после выхода из view
    if request.method in UNSAFE_METHODS:
        log.info("added background task for saving state")
        background_tasks.add_task(storage.save_state)


def api_token_required(
    api_token: Annotated[
        str,
        Query(),
    ],
):
    if api_token not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )
