import logging

from fastapi import (
    APIRouter,
    status,
    Depends,
)

from api.api_v1.short_urls.dependencies import (
    save_storage_state,
    api_token_required,
)
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlRead,
)

from api.api_v1.short_urls.crud import storage


log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
    dependencies=[Depends(save_storage_state)],
)


@router.get(
    "/",
    response_model=list[ShortUrlRead],
)
def read_short_url_list() -> list[ShortUrl]:
    return storage.get()


@router.post(
    "/",
    response_model=ShortUrlRead,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_crate: ShortUrlCreate,
    _=Depends(api_token_required),
) -> ShortUrl:
    return storage.create(short_url_crate)
