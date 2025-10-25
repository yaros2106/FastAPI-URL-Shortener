from typing import Any

from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette.status import HTTP_401_UNAUTHORIZED

from api.api_v1.auth.services import redis_users, utils_jwt
from api.api_v1.auth.services.jwt_helper import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
)
from schemas.user import UserSchema

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/jwt/login",
)


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
) -> UserSchema:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not redis_users.user_exists(username):
        raise HTTPException(
            status_code=404,
            detail=f"User {username!r} not found",
        )
    if not redis_users.validate_user_password(username, password):
        raise unauthed_exc
    return UserSchema(username=username)


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict[str, Any]:
    try:
        payload = utils_jwt.decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token error",
        )
    return payload


def validate_token_type(
    payload: dict[str, Any],
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} when expected {token_type!r}",
    )


def get_user_by_token_subject(
    payload: dict[str, Any],
) -> UserSchema:
    username = payload.get("sub")
    if not redis_users.user_exists(username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="token invalid (user not found)",
        )
    return UserSchema(username=username)


def get_current_auth_user(
    payload=Depends(get_current_token_payload),
) -> UserSchema:
    validate_token_type(
        payload=payload,
        token_type=ACCESS_TOKEN_TYPE,
    )
    return get_user_by_token_subject(payload=payload)


def get_current_auth_user_for_refresh(
    payload=Depends(get_current_token_payload),
) -> UserSchema:
    validate_token_type(
        payload=payload,
        token_type=REFRESH_TOKEN_TYPE,
    )
    return get_user_by_token_subject(payload=payload)
