from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str


class TokenInfoSchema(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
