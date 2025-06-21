import secrets
from abc import ABC, abstractmethod

from redis import Redis

from core import config


class AbstractTokensHelper(ABC):
    """
    Что мне нужно от обертки:
    - проверять на наличие токена
    - добавлять токен в хранилище
    - сгенерировать и добавить токены
    """

    @abstractmethod
    def token_exists(
        self,
        token,
    ) -> bool:
        """
        Check if token exists
        :param token:
        :return:
        """

    @abstractmethod
    def add_token(
        self,
        token,
    ) -> None:
        """
        Save token into storage
        :param token:
        :return:
        """

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe()

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token


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

    def token_exists(self, token) -> bool:
        return bool(
            self.redis.sismember(
                self.token_set_name,
                token,
            )
        )

    def add_token(self, token) -> None:
        self.redis.sadd(
            self.token_set_name,
            token,
        )


redis_tokens = RedisTokensHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    token_set_name=config.REDIS_TOKENS_SET_NAME,
)
