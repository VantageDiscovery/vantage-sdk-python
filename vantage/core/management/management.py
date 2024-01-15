from vantage.core.base import BaseAPI
from vantage.core.management.apis import (
    AccountAPI,
    CollectionAPI,
    ExternalAPIKeysAPI,
    VantageAPIKeysAPI,
)

__all__ = ["ManagementAPI"]


class ManagementAPI(BaseAPI):
    def __init__(self, host: str, api_key: str):
        super().__init__(host, api_key)
        self.account_api = AccountAPI(host, api_key)
        self.collection_api = CollectionAPI(host, api_key)
        self.external_api_keys_api = ExternalAPIKeysAPI(host, api_key)
        self.vantage_api_keys = VantageAPIKeysAPI(host, api_key)
