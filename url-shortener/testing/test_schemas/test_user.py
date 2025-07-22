import os
import pathlib
import sys

import pytest


@pytest.mark.skip(reason="user schema not implemented yet")
def test_user_schema() -> None:
    user_data = {"username": "foobar"}
    assert user_data["username"] == "spam"


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="spip test on windows due some reason",
)
def test_platform() -> None:
    assert sys.platform != "win32"


@pytest.mark.skipif(
    os.name == "posix",
    reason="run only on windows",
)
def test_os_name() -> None:
    assert os.name == "nt"


@pytest.mark.skipif(
    os.name != "posix",
    reason="run only on posix",
)
def test_only_for_unix() -> None:
    path = pathlib.Path(__file__)
    assert isinstance(path, pathlib.PosixPath)
