from fastapi import APIRouter

from .auth.jwt_auth import router as jwt_auth_router
from .short_urls.views import router as short_urls_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(short_urls_router)
router.include_router(jwt_auth_router)
