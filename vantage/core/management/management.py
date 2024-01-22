from __future__ import annotations

from vantage.core.http.api_client import ApiClient
from vantage.core.management.apis import (
    AccountAPI,
    CollectionAPI,
    ExternalAPIKeysAPI,
    VantageAPIKeysAPI,
)


class ManagementAPI:
    def __init__(
        self,
        account_api: AccountAPI,
        collection_api: CollectionAPI,
        external_api_keys_api: ExternalAPIKeysAPI,
        vantage_api_keys_api: VantageAPIKeysAPI,
    ):
        self.account_api = account_api
        self.collection_api = collection_api
        self.external_api_keys_api = external_api_keys_api
        self.vantage_api_keys_api = vantage_api_keys_api

    @classmethod
    def from_defaults(cls, api_client: ApiClient) -> ManagementAPI:
        account_api = AccountAPI(api_client)
        collection_api = CollectionAPI(api_client)
        external_api_keys_api = ExternalAPIKeysAPI(api_client)
        vantage_api_keys_api = VantageAPIKeysAPI(api_client)
        return cls(
            account_api,
            collection_api,
            external_api_keys_api,
            vantage_api_keys_api,
        )
