from __future__ import annotations

from vantage_sdk.core.http.api.account_management_api import (
    AccountManagementApi,
)
from vantage_sdk.core.http.api.collection_management_api import (
    CollectionManagementApi,
)
from vantage_sdk.core.http.api.documents_api import DocumentsApi
from vantage_sdk.core.http.api.external_api_keys_api import ExternalAPIKeysApi
from vantage_sdk.core.http.api.vantage_api_keys_api import VantageAPIKeysApi
from vantage_sdk.core.http.api_client import ApiClient


class ManagementAPI:
    def __init__(
        self,
        account_api: AccountManagementApi,
        collection_api: CollectionManagementApi,
        external_api_keys_api: ExternalAPIKeysApi,
        vantage_api_keys_api: VantageAPIKeysApi,
        documents_api: DocumentsApi,
    ):
        self.account_api = account_api
        self.collection_api = collection_api
        self.external_api_keys_api = external_api_keys_api
        self.vantage_api_keys_api = vantage_api_keys_api
        self.documents_api = documents_api

    @classmethod
    def from_defaults(cls, api_client: ApiClient) -> ManagementAPI:
        account_api = AccountManagementApi(api_client=api_client)
        collection_api = CollectionManagementApi(api_client=api_client)
        external_api_keys_api = ExternalAPIKeysApi(api_client=api_client)
        vantage_api_keys_api = VantageAPIKeysApi(api_client=api_client)
        documents_api = DocumentsApi(api_client=api_client)
        return cls(
            account_api=account_api,
            collection_api=collection_api,
            external_api_keys_api=external_api_keys_api,
            vantage_api_keys_api=vantage_api_keys_api,
            documents_api=documents_api,
        )
