from vantage.core.base import BaseAPI
from vantage.core.http.api.external_api_keys_api import ExternalAPIKeysApi


__all__ = ["ExternalAPIKeysAPI"]


class ExternalAPIKeysAPI(BaseAPI):
    def __init__(
        self, api_key: str, host: str | None, pool_threads: int | None = 1
    ):
        super().__init__(api_key, host, pool_threads)
        self.api = ExternalAPIKeysApi(api_client=self.api_client)
