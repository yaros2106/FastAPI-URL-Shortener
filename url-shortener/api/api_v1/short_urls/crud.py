from pydantic import BaseModel, AnyHttpUrl

from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
)


class ShortUrlsStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def get(self) -> list[ShortUrl]:
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_to_short_url.get(slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_in.model_dump(),
        )
        self.slug_to_short_url[short_url_in.slug] = short_url
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_short_url.pop(slug, None)

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:
        # updated_short_url = short_url.model_copy(
        #     **short_url_in.model_dump(),
        # )
        # self.slug_to_short_url[updated_short_url.slug] = updated_short_url
        # return updated_short_url
        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)

        return short_url


storage = ShortUrlsStorage()

storage.create(
    ShortUrlCreate(
        target_url=AnyHttpUrl("https://example.com"),
        slug="example",
    )
)
storage.create(
    ShortUrlCreate(
        target_url=AnyHttpUrl("https://google.com"),
        slug="search",
    )
)
