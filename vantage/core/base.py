import os
from typing import Optional, Dict


class BaseAPI:
    """Base class for HTTP API calls."""

    def __init__(self, api_key: str, host: Optional[str]):
        self.api_key = api_key
        # TODO: add config and default values
        self.host = (
            host if host else "https://api.dev-a.dev.vantagediscovery.com/"
        )
