from typing import Optional


class BaseAPI:
    """Base class for HTTP API calls."""

    def __init__(self, api_key: str, host: Optional[str]):
        self.api_key = api_key
        self.host = (
            host if host else "default"
        )  # TODO: add config and default values
