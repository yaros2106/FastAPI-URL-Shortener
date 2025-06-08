from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.api_v1.short_urls.crud import storage
from api.api_v1.short_urls.dependencies import prefetch_short_urls
from schemas.short_url import (
    ShortUrl,
    ShortUrlUpdate,
)

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Short URL not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "URL 'slug' not found",
                    },
                },
            },
        }
    },
)

ShortUrlBySlug = Annotated[
    ShortUrl,
    Depends(prefetch_short_urls),
]


@router.get(
    "/",
    response_model=ShortUrl,
)
def read_short_url_details(
    url: ShortUrlBySlug,
) -> ShortUrl:
    return url


@router.put(
    "/",
    response_model=ShortUrl,
)
def update_short_url_details(
    url: ShortUrlBySlug,
    short_url_in: ShortUrlUpdate,
):
    return storage.update(
        short_url=url,
        short_url_in=short_url_in,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_short_url(
    url: ShortUrlBySlug,
) -> None:
    storage.delete(short_url=url)
