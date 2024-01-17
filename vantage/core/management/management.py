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
        account_api: Optional[AccountAPI],
        collection_api: Optional[CollectionAPI],
        external_api_keys_api: Optional[ExternalAPIKeysAPI],
        vantage_api_keys_api: Optional[VantageAPIKeysAPI],
    ):
        super().__init__(api_key, host)
        self.account_api = account_api
        self.collection_api = collection_api
        self.external_api_keys_api = external_api_keys_api
        self.vantage_api_keys_api = vantage_api_keys_api

    @classmethod
    def from_defaults(cls, api_key: str, host: Optional[str]):
        account_api = AccountAPI(api_key, host)
        collection_api = CollectionAPI(api_key, host)
        external_api_keys_api = ExternalAPIKeysAPI(api_key, host)
        vantage_api_keys_api = VantageAPIKeysAPI(api_key, host)
        return cls(
            api_key,
            host,
            account_api,
            collection_api,
            external_api_keys_api,
            vantage_api_keys_api,
        )
