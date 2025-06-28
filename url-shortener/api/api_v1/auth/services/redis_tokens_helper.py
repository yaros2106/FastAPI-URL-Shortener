from redis import Redis

from api.api_v1.auth.services.tokens_helper import AbstractTokensHelper
from core import config


class RedisTokensHelper(AbstractTokensHelper):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        token_set_name: str,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.token_set_name = token_set_name

    def token_exists(
        self,
        token,
    ) -> bool:
        return bool(
            self.redis.sismember(
                self.token_set_name,
                token,
            )
        )

    def add_token(
        self,
        token,
    ) -> None:
        self.redis.sadd(
            self.token_set_name,
            token,
        )

    def get_tokens(self):
        return list(self.redis.smembers(self.token_set_name))


redis_tokens = RedisTokensHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    token_set_name=config.REDIS_TOKENS_SET_NAME,
)
