from os import getenv
from unittest import TestCase

from api.api_v1.auth.services import redis_tokens

if getenv("TESTING") != "1":
    msg = "Environment is not ready for testing"
    raise OSError(msg)


class RedisTokensHelperTestCase(TestCase):
    def test_generate_and_save_token(self) -> None:
        new_token = redis_tokens.generate_and_save_token()
        expected_exists = True
        self.assertEqual(
            expected_exists,
            redis_tokens.token_exists(new_token),
        )
