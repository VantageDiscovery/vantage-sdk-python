"""This module contains ManagementAPI, a class for accessing management API."""

from __future__ import annotations

from vantage_sdk.core.http.api.account_management_api import (
    AccountManagementApi,
)
from vantage_sdk.core.http.api.collection_management_api import (
    CollectionManagementApi,
)
from vantage_sdk.core.http.api.documents_api import DocumentsApi
from vantage_sdk.core.http.api.external_keys_api import ExternalKeysApi
from vantage_sdk.core.http.api.shopping_assistant_api import (
    ShoppingAssistantApi,
)
from vantage_sdk.core.http.api.vantage_api_keys_api import VantageAPIKeysApi
from vantage_sdk.core.http.api.vantage_vibe_api import VantageVibeApi
from vantage_sdk.core.http.api_client import ApiClient


class ManagementAPI:
    """
    Class for accessing Management API.

    Attributes
    ----------
    account_api: AccountManagementApi
        Account management API component.
    collection_api: CollectionManagementApi
        Collection management API component.
    external_api_keys_api: ExternalAPIKeysApi
        External API keys management API component.
    vantage_api_keys_api: VantageAPIKeysApi
        Vantage API keys management API component.
    shopping_assistant_api: ShoppingAssistantApi
        Shopping Assistant management API component.
    vantage_vibe_api: ShoppingAssistantApi
        Vantage Vibe management API component.
    documents_api: DocumentsApi
        Documents management API component.
    """

    def __init__(
        self,
        account_api: AccountManagementApi,
        collection_api: CollectionManagementApi,
        external_keys_api: ExternalKeysApi,
        vantage_api_keys_api: VantageAPIKeysApi,
        shopping_assistant_api: ShoppingAssistantApi,
        vantage_vibe_api: VantageVibeApi,
        documents_api: DocumentsApi,
    ):
        """
        Default constructor.

        Parameters
        ----------
        account_api: AccountManagementApi
            Account management API component.
        collection_api: CollectionManagementApi
            Collection management API component.
        external_api_keys_api: ExternalAPIKeysApi
            External API keys management API component.
        vantage_api_keys_api: VantageAPIKeysApi
            Vantage API keys management API component.
        shopping_assistant_api: ShoppingAssistantApi
            Shopping Assistant management API component.
        vantage_vibe_api: ShoppingAssistantApi
            Vantage Vibe management API component.
        documents_api: DocumentsApi
            Documents management API component.
        """
        self.account_api = account_api
        self.collection_api = collection_api
        self.external_keys_api = external_keys_api
        self.vantage_api_keys_api = vantage_api_keys_api
        self.shopping_assistant_api = shopping_assistant_api
        self.vantage_vibe_api = vantage_vibe_api
        self.documents_api = documents_api

    @classmethod
    def from_defaults(cls, api_client: ApiClient) -> ManagementAPI:
        """
        Constructs ManagementAPI instance using default values.

        This method is the preferred way to construct ManagementAPI instance.

        Parameters
        ----------
        api_client: ApiClient
            API client component used to call the API.

        Returns
        -------
        ManagementAPI
            ManagementAPI instance.
        """
        account_api = AccountManagementApi(api_client=api_client)
        collection_api = CollectionManagementApi(api_client=api_client)
        external_keys_api = ExternalKeysApi(api_client=api_client)
        vantage_api_keys_api = VantageAPIKeysApi(api_client=api_client)
        shopping_assistant_api = ShoppingAssistantApi(api_client=api_client)
        vantage_vibe_api = VantageVibeApi(api_client=api_client)
        documents_api = DocumentsApi(api_client=api_client)
        return cls(
            account_api=account_api,
            collection_api=collection_api,
            external_keys_api=external_keys_api,
            vantage_api_keys_api=vantage_api_keys_api,
            shopping_assistant_api=shopping_assistant_api,
            vantage_vibe_api=vantage_vibe_api,
            documents_api=documents_api,
        )
