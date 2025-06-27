import logging

from pydantic import (
    BaseModel,
    ValidationError,
)
from redis import Redis

from core import config
from core.config import SHORT_URL_STORAGE_FILEPATH
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_SHORT_URLS,
    decode_responses=True,
)


class ShortUrlBaseError(Exception):
    """
    Base exception for short url CRUD actions
    """


class ShortUrlAlreadyExists(ShortUrlBaseError):
    """
    Raised when a short url on creation already exists
    """


class ShortUrlsStorage(BaseModel):

    def save_short_url(self, short_url: ShortUrl) -> None:
        redis.hset(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )

    def get(self) -> list[ShortUrl]:
        data = redis.hvals(name=config.REDIS_SHORT_URLS_HASH_NAME)
        return [ShortUrl.model_validate_json(film) for film in data]

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        if data := redis.hget(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=slug,
        ):
            return ShortUrl.model_validate_json(data)

    def exists(self, slug: str) -> bool:
        return redis.hexists(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=slug,
        )

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_in.model_dump(),
        )
        self.save_short_url(short_url)
        log.info("Created short url %s", short_url)
        return short_url

    def create_or_raise_if_exists(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        if not self.exists(short_url_in.slug):
            return self.create(short_url_in)
        raise ShortUrlAlreadyExists(short_url_in.slug)

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(
            config.REDIS_SHORT_URLS_HASH_NAME,
            slug,
        )

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)
        self.save_short_url(short_url)
        return short_url

    def update_partial(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field_name, value)
        self.save_short_url(short_url)
        return short_url


storage = ShortUrlsStorage()
