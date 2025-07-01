from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from schemas.short_url import ShortUrl

from .api_v1.short_urls.dependencies import prefetch_short_urls

router = APIRouter(
    prefix="/r",
    tags=["Redirect"],
)


@router.get("/{slug}")
@router.get("/{slug/}")
def redirect_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_urls),
    ],
) -> RedirectResponse:
    return RedirectResponse(
        url=str(url.target_url),
    )
