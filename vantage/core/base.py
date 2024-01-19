import os
from typing import Dict, Optional

from vantage.core.http import ApiClient


DEFAULT_HEADERS: Dict[str, str] = {
    "authorization": f"Bearer {os.environ['VANTAGE_TOKEN']}"
}  # TODO: move to config


class BaseAPI:
    """Base class for HTTP API calls."""

    def __init__(
        self,
        api_key: str,
        host: Optional[str] = None,
        pool_threads: Optional[int] = 1,
    ):
        self.api_key = api_key
        # TODO: add config and default values
        self.host = (
            host if host else "https://api.dev-a.dev.vantagediscovery.com/"
        )
        self.api_client = ApiClient(pool_threads=pool_threads)
        for k, v in DEFAULT_HEADERS.items():
            self.api_client.set_default_header(k, v)
