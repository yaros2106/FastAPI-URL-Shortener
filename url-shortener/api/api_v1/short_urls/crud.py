from pydantic import (
    BaseModel,
    ValidationError,
)

from core.config import SHORT_URL_STORAGE_FILEPATH
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)


class ShortUrlsStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def save_state(self) -> None:
        SHORT_URL_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))

    @classmethod
    def from_state(cls) -> "ShortUrlsStorage":
        if not SHORT_URL_STORAGE_FILEPATH.exists():
            return ShortUrlsStorage()
        return cls.model_validate_json(SHORT_URL_STORAGE_FILEPATH.read_text())

    def get(self) -> list[ShortUrl]:
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_to_short_url.get(slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_in.model_dump(),
        )
        self.slug_to_short_url[short_url_in.slug] = short_url
        self.save_state()
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_short_url.pop(slug, None)
        self.save_state()

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)
        self.save_state()
        return short_url

    def update_partial(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field_name, value)
        self.save_state()
        return short_url


try:
    storage = ShortUrlsStorage.from_state()
except ValidationError:
    storage = ShortUrlsStorage()
    storage.save_state()
