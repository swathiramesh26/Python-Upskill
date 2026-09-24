import requests


class BaseURLSession(requests.Session):
    def __init__(self, base_url: str):
        super().__init__()
        if not base_url:
            raise ValueError(
                "BaseURLSession requires a non-empty base_url "
                "(check that API_BASE_URL is set, e.g. in .env)"
            )
        self.base_url = base_url.rstrip("/")

    def request(self, method, url, *args, **kwargs):
        full_url = (
            url if url.startswith(("http://", "https://"))
            else f"{self.base_url}{url}"
        )
        return super().request(method, full_url, *args, **kwargs)