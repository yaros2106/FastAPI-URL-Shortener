from unittest import TestCase

from schemas.short_url import ShortUrl, ShortUrlCreate


class ShortUrlCreateTestCase(TestCase):
    def test_short_url_can_be_created_from_create_schema(self) -> None:
        short_url_in = ShortUrlCreate(
            slug="some-slug",
            description="some-description",
            target_url="https://example.com",
        )
        short_url = ShortUrl(
            **short_url_in.model_dump(),
        )
        self.assertEqual(
            short_url_in.slug,
            short_url.slug,
        )
        self.assertEqual(
            short_url_in.target_url,
            short_url.target_url,
        )
        self.assertEqual(
            short_url_in.description,
            short_url.description,
        )

    def test_short_url_accepts_different_urls(self) -> None:
        urls = [
            "https://example.com/",
            "http://example.com",
            "http://www.example.com",
            "http://abc.example.com",
            # "rtmp://video.example.com",
            # "rtmps://video.example.com",
            "https://abc.example.com/foo/bar/",
        ]

        for url in urls:
            with self.subTest(url=url, msg=f"test-url: {url}"):
                short_url_create = ShortUrlCreate(
                    slug="some-slug",
                    description="some-description",
                    target_url=url,
                )
                self.assertEqual(
                    url.rstrip("/"),
                    short_url_create.model_dump(mode="json")["target_url"].rstrip("/"),
                )
