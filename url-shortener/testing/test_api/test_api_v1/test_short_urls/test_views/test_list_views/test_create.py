import random
import string

from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.short_url import ShortUrl, ShortUrlCreate


def test_create_short_url(auth_client: TestClient) -> None:
    url = app.url_path_for("create_short_url")
    short_url_create = ShortUrlCreate(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
        description="A short url",
        target_url="https://example.com",
    )
    data: dict[str, str] = short_url_create.model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_values = ShortUrlCreate(**response_data)
    assert received_values == short_url_create, response_data


def test_create_short_url_already_exists(
    short_url: ShortUrl,
    auth_client: TestClient,
) -> None:
    url = app.url_path_for("create_short_url")
    existing_short_url = short_url.model_dump(mode="json")
    short_url_in = ShortUrlCreate(**existing_short_url).model_dump(mode="json")
    response = auth_client.post(url=url, json=short_url_in)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_data = response.json()
    expected_error = f"Short URL with slug='{short_url.slug}' already exists."
    assert response_data["detail"] == expected_error, response_data
