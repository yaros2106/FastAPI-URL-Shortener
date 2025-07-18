from typing import ClassVar
from unittest import TestCase

import pytest

from api.api_v1.short_urls.crud import (
    ShortUrlAlreadyExistsError,
    storage,
)
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlPartialUpdate,
    ShortUrlUpdate,
)
from testing.conftest import create_short_url_random_slug


class ShortUrlsStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.short_url = create_short_url_random_slug()

    def tearDown(self) -> None:
        storage.delete(self.short_url)

    def test_update(self) -> None:
        short_url_update = ShortUrlUpdate(
            **self.short_url.model_dump(),
        )
        short_url_update.description = "new description"
        source_description = self.short_url.description
        updated_short_url = storage.update(
            short_url=self.short_url,
            short_url_in=short_url_update,
        )
        self.assertNotEqual(
            source_description,
            updated_short_url.description,
        )
        self.assertEqual(
            short_url_update,
            ShortUrlUpdate(**updated_short_url.model_dump()),
        )

    def test_update_partial(self) -> None:
        short_url_partial_update = ShortUrlPartialUpdate(
            description="new description",
        )
        source_description = self.short_url.description
        updated_partial_short_url = storage.update_partial(
            short_url=self.short_url,
            short_url_in=short_url_partial_update,
        )
        self.assertNotEqual(
            source_description,
            updated_partial_short_url.description,
        )
        self.assertEqual(
            short_url_partial_update.description,
            updated_partial_short_url.description,
        )


class ShortUrlsStorageGetShortUrlsTestCase(TestCase):
    SHORT_URLS_COUNT = 3
    short_urls: ClassVar[list[ShortUrl]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.short_urls = [
            create_short_url_random_slug() for _ in range(cls.SHORT_URLS_COUNT)
        ]

    @classmethod
    def tearDownClass(cls) -> None:
        for short_url in cls.short_urls:
            storage.delete(short_url)

    def test_get_list(self) -> None:
        db_short_urls = storage.get()
        expected_slugs = {su.slug for su in self.short_urls}  # {a, b, c}
        slugs = {su.slug for su in db_short_urls}  # {a, b, c, d, e}
        expected_diff: set[str] = set()
        diff = expected_slugs - slugs  # {} если все полученные есть в ожидаемых
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for short_url in self.short_urls:
            with self.subTest(
                slug=short_url.slug,
                msg=f"checking: {short_url.slug}",
            ):
                db_short_url = storage.get_by_slug(short_url.slug)
                self.assertEqual(
                    short_url,
                    db_short_url,
                )


def test_create_or_raise_if_exists(short_url: ShortUrl) -> None:
    short_url_create = ShortUrlCreate(**short_url.model_dump())
    with pytest.raises(
        ShortUrlAlreadyExistsError,
        match=short_url_create.slug,
    ) as exc_info:
        storage.create_or_raise_if_exists(short_url_create)

    assert exc_info.value.args[0] == short_url_create.slug
