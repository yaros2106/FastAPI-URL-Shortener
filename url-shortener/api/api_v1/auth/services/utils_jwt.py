from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    PRIVATE_KEY_PATH,
    PUBLIC_KEY_PATH,
)


def encode_jwt(
    payload: dict[str, Any],
    private_key: str = PRIVATE_KEY_PATH.read_text(),
    algorithm: str = ALGORITHM,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
) -> dict[str, Any]:
    to_encode = payload.copy()
    now = datetime.now(UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = PUBLIC_KEY_PATH.read_text(),
    algorithm: str = ALGORITHM,
) -> dict[str, Any]:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded
