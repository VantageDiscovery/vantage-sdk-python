from __future__ import annotations

from typing import Optional

from vantage.core.base import BaseAPI
from vantage.core.management.apis import (
    AccountAPI,
    CollectionAPI,
    ExternalAPIKeysAPI,
    VantageAPIKeysAPI,
)


class ManagementAPI(BaseAPI):
    def __init__(
        self,
        api_key: str,
        account_api: AccountAPI,
        collection_api: CollectionAPI,
        external_api_keys_api: ExternalAPIKeysAPI,
        vantage_api_keys_api: VantageAPIKeysAPI,
        host: Optional[str] = None,
    ):
        super().__init__(api_key, host)
        self.account_api = account_api
        self.collection_api = collection_api
        self.external_api_keys_api = external_api_keys_api
        self.vantage_api_keys_api = vantage_api_keys_api

    @classmethod
    def from_defaults(cls, api_key: str, host: Optional[str]) -> ManagementAPI:
        account_api = AccountAPI(api_key, host)
        collection_api = CollectionAPI(api_key, host)
        external_api_keys_api = ExternalAPIKeysAPI(api_key, host)
        vantage_api_keys_api = VantageAPIKeysAPI(api_key, host)
        return cls(
            api_key,
            account_api,
            collection_api,
            external_api_keys_api,
            vantage_api_keys_api,
            host,
        )
