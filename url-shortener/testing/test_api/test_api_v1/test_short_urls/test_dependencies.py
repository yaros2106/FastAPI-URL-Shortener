from api.api_v1.short_urls.dependencies import UNSAFE_METHODS


class TestUnsafeMethods:

    def test_dont_contain_save_methods(self) -> None:
        save_methods = {
            "GET",
            "HEAD",
            "OPTIONS",
        }
        assert not UNSAFE_METHODS & save_methods

    def test_all_methods_are_upper(self) -> None:
        assert all(method.isupper() for method in UNSAFE_METHODS)
