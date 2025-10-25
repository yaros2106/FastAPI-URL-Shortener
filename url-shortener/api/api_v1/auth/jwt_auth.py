from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from api.api_v1.auth.services.jwt_helper import (
    create_access_token,
    create_refresh_token,
)
from api.api_v1.auth.services.validation import (
    get_current_auth_user,
    get_current_auth_user_for_refresh,
    get_current_token_payload,
    validate_auth_user,
)
from schemas.user import TokenInfoSchema, UserSchema

http_bearer = HTTPBearer(
    scheme_name="JWT",
    description="Your **JWT token**",
    auto_error=False,
)
router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


@router.post(
    "/login",
    response_model=TokenInfoSchema,
)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
) -> TokenInfoSchema:
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenInfoSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/user/me")
def auth_user_check_self_info(
    user: UserSchema = Depends(get_current_auth_user),
    payload=Depends(get_current_token_payload),
) -> dict[str, Any]:
    iat = payload.get("iat")
    return {
        "username": user.username,
        "logged_in": iat,
    }


@router.post(
    "/refresh/",
    response_model=TokenInfoSchema,
    response_model_exclude_none=True,
)
def auth_refresh(
    user: UserSchema = Depends(get_current_auth_user_for_refresh),
) -> TokenInfoSchema:
    access_token = create_access_token(user=user)
    return TokenInfoSchema(access_token=access_token)
