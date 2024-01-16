from typing import Optional

from vantage.core.base import BaseAPI
from vantage.core.management.apis import (
    AccountAPI,
    CollectionAPI,
    ExternalAPIKeysAPI,
    VantageAPIKeysAPI,
)


__all__ = ["ManagementAPI"]


class ManagementAPI(BaseAPI):
    def __init__(
        self,
        api_key: str,
        host: Optional[str],
    ):
        super().__init__(api_key, host)
        self.account_api = AccountAPI(api_key, host)
        self.collection_api = CollectionAPI(api_key, host)
        self.external_api_keys_api = ExternalAPIKeysAPI(api_key, host)
        self.vantage_api_keys = VantageAPIKeysAPI(api_key, host)
