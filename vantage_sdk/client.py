"""
This module contains VantageClient class,
which is a main entry point for users using the SDK.
"""

from __future__ import annotations

import json
import ntpath
import uuid
from os.path import exists
from pathlib import Path
from typing import List, Optional, Union

import magic
import requests

from vantage_sdk.config import (
    API_HOST_VERSION,
    AUTH_ENDPOINT,
    DEFAULT_API_HOST,
    DEFAULT_AUTH_HOST,
    DEFAULT_ENCODING,
)
from vantage_sdk.core.base import AuthorizationClient, AuthorizedApiClient
from vantage_sdk.core.http.models import (
    AccountModifiable,
    CollectionModifiable,
    CollectionStatus,
    CreateCollectionRequest,
    EmbeddingSearchQuery,
    ExternalKeyModifiable,
)
from vantage_sdk.core.http.models import FacetRange as pydantic_FacetRange
from vantage_sdk.core.http.models import (
    MLTheseTheseInner,
    MoreLikeTheseQuery,
    MoreLikeThisQuery,
    SearchOptionsCollection,
    SearchOptionsFacetsInner,
    SearchOptionsFieldValueWeighting,
    SearchOptionsFilter,
    SearchOptionsPagination,
    SearchOptionsSort,
)
from vantage_sdk.core.http.models import (
    SecondaryExternalAccount as OpenAPISecondaryExternalAccount,
)
from vantage_sdk.core.http.models import (
    SemanticSearchQuery,
    ShoppingAssistant,
    ShoppingAssistantModifiable,
    ShoppingAssistantQuery,
    ShoppingAssistantResult,
    TotalCountResult,
    VantageAPIKeyModifiable,
    VantageVibe,
    VantageVibeImage,
    VantageVibeModifiable,
    VantageVibeSearchQuery,
)
from vantage_sdk.core.management import ManagementAPI
from vantage_sdk.core.search import SearchAPI
from vantage_sdk.core.text_util import (
    BatchTextFileReader,
    TextSplitter,
    count_lines,
)
from vantage_sdk.core.validation import VALIDATOR as validator
from vantage_sdk.exceptions import VantageFileUploadError, VantageValueError
from vantage_sdk.model.account import Account
from vantage_sdk.model.collection import (
    Collection,
    CollectionUploadURL,
    HuggingFaceCollection,
    OpenAICollection,
    UserProvidedEmbeddingsCollection,
)
from vantage_sdk.model.document import (
    UserProvidedEmbeddingsDocument,
    VantageManagedEmbeddingsDocument,
)
from vantage_sdk.model.keys import (
    AnthropicKey,
    ExternalKey,
    LLMProvider,
    OpenAIKey,
    SecondaryExternalAccount,
    VantageAPIKey,
    VantageAPIKeyRole,
)
from vantage_sdk.model.search import (
    ApproximateResultsCountResult,
    Facet,
    FieldValueWeighting,
    Filter,
    MoreLikeTheseItem,
    Pagination,
    SearchOptions,
    SearchResult,
    Sort,
    TotalCountsOptions,
    VantageVibeImageBase64,
    VantageVibeImageUrl,
)
from vantage_sdk.model.validation import CollectionType, ValidationError


_DOCUMENTS_UPLOAD_BATCH_SIZE = 500
_PARQUET_FILE_TYPE = "Apache Parquet"
_JSONL_MIME_TYPE = "application/x-ndjson"
_JSON_MIME_TYPE = "application/json"


class VantageClient:
    def __init__(
        self,
        management_api: ManagementAPI,
        search_api: SearchAPI,
        account_id: str,
        vantage_api_key: Optional[str] = None,
        host: Optional[str] = DEFAULT_API_HOST,
    ) -> None:
        """
        Initializes a new instance of the VantageClient class, the main
        entry point for interacting with Vantage Discovery via the Python SDK,
        setting up the necessary APIs for management and search operations.

        Parameters
        ----------
        management_api : ManagementAPI
            An instance of the ManagementAPI class.
        search_api : SearchAPI
            An instance of the SearchAPI class.
        account_id : str
            The account ID to be used for all operations within the Vantage platform.
        vantage_api_key : Optional[str], optional
            An optional Vantage API key used for search operations.
            If not provided, must be set elsewhere before performing those operations.
            Defaults to None.
        host : Optional[str], optional
            The host URL for the Vantage API.
            If not provided, a default value is used.
        """

        self.management_api = management_api
        self.search_api = search_api
        self.account_id = account_id
        self.vantage_api_key = vantage_api_key
        self.host = host
        self._default_encoding = DEFAULT_ENCODING

    @classmethod
    def using_vantage_api_key(
        cls,
        vantage_api_key: str,
        account_id: str,
        api_host: Optional[str] = DEFAULT_API_HOST,
    ) -> VantageClient:
        """
        Instantiates a VantageClient using a Vantage API key for authentication.

        Parameters
        ----------
        vantage_api_key : str
            The Vantage API key for authenticating API requests.
        account_id : str
            The account ID associated with the Vantage operations.
        api_host : Optional[str], optional
            The host URL for the Vantage API.
            If not provided, a default value is used.

        Returns
        -------
        VantageClient
            An instance of the VantageClient.
        """
        host = f"{api_host}"

        auth_client = AuthorizationClient.using_provided_vantage_api_key(
            vantage_api_key=vantage_api_key
        )

        api_client = AuthorizedApiClient(authorization_client=auth_client)

        if host is not None:
            api_client.configuration.host = host

        management_api = ManagementAPI.from_defaults(api_client=api_client)
        search_api = SearchAPI(api_client=api_client)

        return cls(
            management_api=management_api,
            search_api=search_api,
            account_id=account_id,
            vantage_api_key=vantage_api_key,
            host=host,
        )

    @classmethod
    def using_jwt_token(
        cls,
        vantage_api_jwt_token: str,
        account_id: str,
        vantage_api_key: Optional[str] = None,
        api_host: Optional[str] = DEFAULT_API_HOST,
    ) -> VantageClient:
        """
        Instantiates a VantageClient using a JWT token for authentication.

        Parameters
        ----------
        vantage_api_jwt_token : str
            The JWT token for authenticating API requests.
        account_id : str
            The account ID associated with the Vantage operations.
        vantage_api_key : Optional[str], optional
            An optional Vantage API key used for search operations.
            If not provided, must be set elsewhere before performing those operations.
            Defaults to None.
        api_host : Optional[str], optional
            The host URL for the Vantage API.
            If not provided, a default value is used.

        Returns
        -------
        VantageClient
            An instance of the VantageClient.
        """
        host = f"{api_host}/{API_HOST_VERSION}"

        auth_client = AuthorizationClient.using_provided_token(
            vantage_jwt_token=vantage_api_jwt_token
        )

        api_client = AuthorizedApiClient(authorization_client=auth_client)

        if host is not None:
            api_client.configuration.host = host

        management_api = ManagementAPI.from_defaults(api_client=api_client)
        search_api = SearchAPI(api_client=api_client)

        return cls(
            management_api=management_api,
            search_api=search_api,
            account_id=account_id,
            vantage_api_key=vantage_api_key,
            host=host,
        )

    @classmethod
    def using_client_credentials(
        cls,
        vantage_client_id: str,
        vantage_client_secret: str,
        account_id: str,
        vantage_api_key: Optional[str] = None,
        api_host: Optional[str] = DEFAULT_API_HOST,
        auth_host: Optional[str] = DEFAULT_AUTH_HOST,
    ) -> VantageClient:
        """
        Instantiates a VantageClient using OAuth client credentials for authentication.

        This class method simplifies the process of creating a `VantageClient` instance
        by handling OAuth authentication automatically, using the provided client ID and secret.

        Parameters
        ----------
        vantage_client_id : str
            The client ID issued by Vantage for OAuth authentication.
        vantage_client_secret : str
            The client secret issued by Vantage for OAuth authentication.
        account_id : str
            The account ID to be used with the Vantage operations.
        vantage_api_key : Optional[str], optional
            An optional Vantage API key used for search operations.
            If not provided, must be set elsewhere before performing those operations.
            Defaults to None.
        api_host : Optional[str], optional
            The host URL for the Vantage API.
            If not provided, a default value is used.
        auth_host : Optional[str], optional
            The base URL of the Vantage authentication server.
            If not provided, a default value is used.

        Returns
        -------
        VantageClient
            An instance of the VantageClient.

        Notes
        -----
        - The method performs authentication with the Vantage OAuth server
        automatically and configures the internal API client with the obtained access token.
        """
        host = f"{api_host}/{API_HOST_VERSION}"
        auth_endpoint = f"{auth_host}{AUTH_ENDPOINT}"

        auth_client = AuthorizationClient.automatic_token_management(
            vantage_client_id=vantage_client_id,
            vantage_client_secret=vantage_client_secret,
            sso_endpoint_url=auth_endpoint,
            vantage_audience_url=api_host,
        )

        auth_client.authenticate()
        api_client = AuthorizedApiClient(authorization_client=auth_client)

        if host is not None:
            api_client.configuration.host = host

        management_api = ManagementAPI.from_defaults(api_client=api_client)
        search_api = SearchAPI(api_client=api_client)

        return cls(
            management_api=management_api,
            search_api=search_api,
            account_id=account_id,
            vantage_api_key=vantage_api_key,
            host=host,
        )

    # region Account

    def get_account(
        self,
        account_id: Optional[str] = None,
    ) -> Account:
        """
        Retrieves the details of an account.

        Parameters
        ----------
        account_id : Optional[str], optional
            The unique identifier of the account to be retrieved.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        Account
            An Account object containing the details of the requested account.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        result = self.management_api.account_api.get_account(
            account_id=account_id or self.account_id
        )
        return Account.model_validate(result.model_dump())

    def update_account(
        self,
        account_name: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> Account:
        """
        Updates the account.

        Parameters
        ----------
        account_name : Optional[str], optional
            The new name for the account.
        account_id : Optional[str], optional
            The unique identifier of the account to be updated.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        Account
            An updated Account object reflecting the changes made.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        account_modifiable = AccountModifiable(account_name=account_name)

        result = self.management_api.account_api.update_account(
            account_id=account_id or self.account_id,
            account_modifiable=account_modifiable,
        )
        return Account.model_validate(result.model_dump())

    # endregion

    # region Vantage API keys

    def get_vantage_api_keys(
        self,
        account_id: Optional[str] = None,
    ) -> List[VantageAPIKey]:
        """
        Retrieves a list of Vantage API keys for a specified account.

        Parameters
        ----------
        account_id : Optional[str], optional
            The unique identifier of the account for which the Vantage API keys are to be retrieved.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        List[VantageAPIKey]
            A list of VantageAPIKey objects, each representing a Vantage API key associated with the account.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        keys = self.management_api.vantage_api_keys_api.get_vantage_api_keys(
            account_id=account_id or self.account_id,
        )

        return [VantageAPIKey.model_validate(key.model_dump()) for key in keys]

    def get_vantage_api_key(
        self,
        vantage_api_key_id: str,
        account_id: Optional[str] = None,
    ) -> VantageAPIKey:
        """
        Retrieves a specific Vantage API key for a given account.

        Parameters
        ----------
        vantage_api_key_id : str
            The unique identifier of the Vantage API key to be retrieved.
        account_id : Optional[str], optional
            The unique identifier of the account for which the Vantage API key is associated.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        VantageAPIKey
            A VantageAPIKey object containing the details of the requested API key.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        key = self.management_api.vantage_api_keys_api.get_vantage_api_key(
            account_id=account_id or self.account_id,
            vantage_api_key_id=vantage_api_key_id,
        )
        return VantageAPIKey.model_validate(key.model_dump())

    def create_vantage_api_key(
        self,
        name: str,
        roles: List[VantageAPIKeyRole],
        account_id: Optional[str] = None,
    ) -> VantageAPIKey:
        """
        Created new Vantage API key for a given account.

        Parameters
        ----------
        name : str
            Name of the Vantage API key.
        roles : List[VantageAPIKeyRole]
            List of Vantage API key roles that determines usage of the specific key.
        account_id : Optional[str], optional
            The unique identifier of the account for which the Vantage API key is associated.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        VantageAPIKey
            A VantageAPIKey object containing the details of the created API key.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        vantage_api_key_modifiable = VantageAPIKeyModifiable(
            name=name, roles=[role.value for role in roles]
        )

        key = self.management_api.vantage_api_keys_api.create_vantage_api_key(
            account_id=account_id or self.account_id,
            vantage_api_key_modifiable=vantage_api_key_modifiable,
        )
        return VantageAPIKey.model_validate(key.model_dump())

    def revoke_vantage_api_key(
        self,
        vantage_api_key_id: str,
        account_id: Optional[str] = None,
    ) -> None:
        """
        Deactivates a specific Vantage API key for a given account.

        Parameters
        ----------
        vantage_api_key_id : str
            The unique identifier of the Vantage API key to be deactivated.
        account_id : Optional[str], optional
            The unique identifier of the account for which the Vantage API key is associated.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        None

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """
        self.management_api.vantage_api_keys_api.revoke_vantage_api_key(
            account_id=account_id or self.account_id,
            vantage_api_key_id=vantage_api_key_id,
        )

    # endregion

    # region External API keys

    def get_external_keys(
        self,
        account_id: Optional[str] = None,
    ) -> List[ExternalKey]:
        """
        Retrieves a list of external keys associated with a given account.

        Parameters
        ----------
        account_id : Optional[str], optional
            The unique identifier of the account for which the external keys are to be retrieved.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        List[ExternalKey]
            A list of ExternalKey objects, each representing an external key associated with the account.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        keys = self.management_api.external_keys_api.get_external_keys(
            account_id=account_id or self.account_id,
        )
        return [ExternalKey.model_validate(key.model_dump()) for key in keys]

    def get_external_key(
        self,
        external_key_id: str,
        account_id: Optional[str] = None,
    ) -> ExternalKey:
        """
        Retrieves a specific external key associated with a given account.

        Parameters
        ----------
        external_key_id : str
            The unique identifier of the external key to be retrieved.
        account_id : Optional[str], optional
            The unique identifier of the account to which the external key is associated.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        ExternalKey
            An ExternalKey object containing the details of the requested external key.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        key = self.management_api.external_keys_api.get_external_key(
            account_id=account_id or self.account_id,
            external_key_id=external_key_id,
        )

        return ExternalKey.model_validate(key.model_dump())

    def create_external_key(
        self,
        llm_provider: LLMProvider,
        llm_secret: str,
        account_id: Optional[str] = None,
    ) -> ExternalKey:
        """
        Creates a new external key associated with a given account.

        Parameters
        ----------
        llm_provider : LLMProvider
            The provider of the Large Language Model (LLM).
        llm_secret : str
            The secret key for accessing the LLM.
        account_id : Optional[str], optional
            The unique identifier of the account for which the external key is to be created.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        ExternalKey
            An ExternalKey object containing the details of the newly created key.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        external_key_modifiable = ExternalKeyModifiable(
            llm_provider=llm_provider.value, llm_secret=llm_secret
        )

        key = self.management_api.external_keys_api.create_external_key(
            account_id=account_id or self.account_id,
            external_key_modifiable=external_key_modifiable,
        )

        return ExternalKey.model_validate(key.model_dump())

    def update_external_key(
        self,
        external_key_id: str,
        llm_provider: LLMProvider,
        llm_secret: str,
        account_id: Optional[str] = None,
    ) -> ExternalKey:
        """
        Updates the details of a specific external key associated with a given account.

        Parameters
        ----------
        external_key_id : str
            The unique identifier of the external key to be updated.
        llm_provider : LLMProvider
            The new provider of the Large Language Model (LLM).
        llm_secret : str
            The new secret key for accessing the LLM.
        account_id : Optional[str], optional
            The unique identifier of the account to which the external key is associated.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        ExternalKey
            An ExternalKey object containing the updated details of the external key.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        external_key_modifiable = ExternalKeyModifiable(
            llm_provider=llm_provider.value, llm_secret=llm_secret
        )

        key = self.management_api.external_keys_api.update_external_key(
            account_id=account_id or self.account_id,
            external_key_id=external_key_id,
            external_key_modifiable=external_key_modifiable,
        )

        return ExternalKey.model_validate(key.model_dump())

    def delete_external_key(
        self,
        external_key_id: str,
        account_id: Optional[str] = None,
    ) -> None:
        """
        Deletes a specific external key associated with a given account.

        Parameters
        ----------
        external_key_id : str
            The unique identifier of the external key to be deleted.
        account_id : Optional[str], optional
            The unique identifier of the account to which the external key is associated.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        self.management_api.external_keys_api.delete_external_key(
            account_id=account_id or self.account_id,
            external_key_id=external_key_id,
        )

    # endregion

    # region Collections Helper Functions

    def _get_direct_upload_url(
        self,
        collection_id: str,
        file_size: int,
        parquet_file_name: str,
        account_id: Optional[str] = None,
    ) -> CollectionUploadURL:
        """
        Retrieves a direct upload URL for uploading files to a specified collection.

        Parameters
        ----------
        collection_id : str
            The identifier of the collection to which the file is being uploaded.
        file_size : int
            The size of the file to be uploaded, in bytes.
        parquet_file_name : str
            The name of the parquet file being uploaded, used as a customer batch identifier.
        account_id : Optional[str], optional
            The account identifier under which the collection exists.
            If not provided, the default account associated with the user is used.
            Defaults to None.

        Returns
        -------
        CollectionUploadURL
            An object representing the upload URL and any other relevant data needed for the upload process.
        """

        url = self.management_api.collection_api.get_browser_upload_url(
            collection_id=collection_id,
            file_size=file_size,
            customer_batch_identifier=parquet_file_name,
            account_id=account_id or self.account_id,
        )

        return CollectionUploadURL.model_validate(url.model_dump())

    # endregion

    # region Collections

    def list_collections(
        self,
        account_id: Optional[str] = None,
    ) -> List[Collection]:
        """
        Retrieves a list of collections associated with a given account.

        Parameters
        ----------
        account_id : Optional[str], optional
            The unique identifier of the account for which the collections are to be retrieved.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        List[Collection]
            A list of Collection objects, each representing a collection associated with the account.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        collections = self.management_api.collection_api.list_collections(
            account_id=account_id or self.account_id
        )

        return [
            Collection.model_validate(collection.model_dump())
            for collection in collections
        ]

    def get_collection(
        self,
        collection_id: str,
        account_id: Optional[str] = None,
    ) -> Collection:
        """
        Retrieves the details of a specified collection.

        Parameters
        ----------
        collection_id : str
            The unique identifier of the collection to be retrieved.
        account_id : Optional[str], optional
            The account ID to which the collection belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        Collection
            A Collection object containing the details of the specified collection.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        collection = self.management_api.collection_api.get_collection(
            collection_id=collection_id,
            account_id=account_id or self.account_id,
        )

        return Collection.model_validate(collection.model_dump())

    def get_collection_status(
        self,
        collection_id: str,
        account_id: Optional[str] = None,
    ) -> CollectionStatus:
        """
        Retrieves the status of a specified collection.

        Parameters
        ----------
        collection_id : str
            The unique identifier of the collection to be retrieved.
        account_id : Optional[str], optional
            The account ID to which the collection belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        CollectionStatus
            A CollectionStatus object containing the status of the specified collection.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """
        collection_status = (
            self.management_api.collection_api.get_collection_status(
                collection_id=collection_id,
                account_id=account_id or self.account_id,
            )
        )

        return CollectionStatus.model_validate(collection_status.model_dump())

    def create_collection(
        self,
        collection: Union[
            UserProvidedEmbeddingsCollection,
            OpenAICollection,
            HuggingFaceCollection,
        ],
        account_id: Optional[str] = None,
    ) -> Union[
        UserProvidedEmbeddingsCollection,
        OpenAICollection,
        HuggingFaceCollection,
    ]:
        """
        Creates a new collection based on the provided Collection object.

        Parameters
        ----------
        collection : Collection
            Instance of a UserProvidedEmbeddingsCollection, which creates and uses
            embeddings provided by the user, or instance of OpenAICollection /
            HuggingFaceCollection, both of which create and use Vantage-managed embeddings.

        Returns
        -------
        Collection
            A Collection object representing the newly created collection.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        if (
            hasattr(collection, "secondary_external_accounts")
            and collection.secondary_external_accounts is not None
        ):
            collection.secondary_external_accounts = [
                OpenAPISecondaryExternalAccount(
                    external_account_id=account.external_account_id,
                    external_type=account.external_type,
                )
                for account in collection.secondary_external_accounts
            ]

        external_key_id = None
        if (
            hasattr(collection, "external_key")
            and collection.external_key is not None
        ):
            external_key_id = collection.external_key.external_key_id

        create_collection_request = CreateCollectionRequest(
            collection_id=collection.collection_id,
            collection_name=collection.collection_name,
            user_provided_embeddings=bool(collection.user_provided_embeddings),
            embeddings_dimension=int(collection.embeddings_dimension),
            external_key_id=external_key_id,
            secondary_external_accounts=getattr(
                collection, 'secondary_external_accounts', None
            ),
            llm=getattr(collection, 'llm', None),
            llm_secret=getattr(collection, 'llm_secret', None),
            llm_provider=getattr(collection, 'llm_provider', None),
            external_url=getattr(collection, 'external_url', None),
            collection_preview_url_pattern=getattr(
                collection, 'collection_preview_url_pattern', None
            ),
        )

        collection = self.management_api.collection_api.create_collection(
            create_collection_request=create_collection_request,
            account_id=account_id or self.account_id,
        )

        return collection.model_validate(collection.model_dump())

    def update_collection(
        self,
        collection_id: str,
        collection_name: Optional[str] = None,
        external_key_id: Optional[str] = None,
        secondary_external_accounts: Optional[
            List[SecondaryExternalAccount]
        ] = None,
        account_id: Optional[str] = None,
    ) -> Collection:
        """
        Updates an existing collection's details
        identified by its collection_id within a specified account.

        Parameters
        ----------
        collection_id : str
            Unique identifier of the collection to be updated.
        collection_name : Optional[str], optional
            New name for the collection, if updating.
        external_key_id : Optional[str], optional
            New external key ID, if updating.
        secondary_external_accounts: Optional[List[SecondaryExternalAccount]], optional
            Additional external accounts/keys used for indexing, search or both.
            Applicable if llm_provider is set to OpenAI.
        account_id : Optional[str], optional
            Account ID to which the collection belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        Collection
            A Collection object representing the updated collection.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        collection = self.management_api.collection_api.get_collection(
            collection_id=collection_id,
            account_id=account_id or self.account_id,
        )

        if secondary_external_accounts:
            if collection.user_provided_embeddings:
                raise ValueError(
                    "Collections with user-provided embeddings cannot have secondary external accounts."
                )

            if collection.llm_provider is not LLMProvider.OpenAI.value:
                raise ValueError(
                    f"Only collections which are using {LLMProvider.OpenAI.value} as LLM provider can have secondary external accounts."  # noqa: E501
                )

            secondary_external_accounts = [
                OpenAPISecondaryExternalAccount(
                    external_account_id=account.external_account_id,
                    external_type=account.external_type,
                )
                for account in secondary_external_accounts
            ]

        collection_modifiable = CollectionModifiable(
            external_key_id=external_key_id,
            secondary_external_accounts=secondary_external_accounts,
            collection_name=collection_name,
        )

        collection = self.management_api.collection_api.update_collection(
            collection_id=collection_id,
            collection_modifiable=collection_modifiable,
            account_id=account_id or self.account_id,
        )

        return Collection.model_validate(collection.model_dump())

    def delete_collection(
        self,
        collection_id: str,
        account_id: Optional[str] = None,
    ) -> None:
        """
        Deletes a specific collection
        identified by its collection_id within a specified account.

        Parameters
        ----------
        collection_id : str
            The unique identifier of the collection to be deleted.
        account_id : Optional[str], optional
            The account ID to which the collection belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        Collection
            A Collection object representing the collection that was deleted.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        self.management_api.collection_api.delete_collection(
            collection_id=collection_id,
            account_id=account_id if account_id else self.account_id,
        )

    # endregion

    # region Shopping Assistant

    def list_shopping_assistants(
        self,
        account_id: Optional[str] = None,
    ) -> List[ShoppingAssistant]:
        """
        Retrieves a list of shopping assistants associated with a given account.

        Parameters
        ----------
        account_id : Optional[str], optional
            The unique identifier of the account for which the shopping assistants are to be retrieved.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        List[ShoppingAssistant]
            A list of ShoppingAssistant objects.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        shopping_assistants = self.management_api.shopping_assistant_api.list_shopping_assistants(
            account_id=account_id or self.account_id,
        )

        return [
            ShoppingAssistant.model_validate(assistant.model_dump())
            for assistant in shopping_assistants
        ]

    def get_shopping_assistant(
        self,
        shopping_assistant_id: str,
        account_id: Optional[str] = None,
    ) -> ShoppingAssistant:
        """
        Retrieves the details of a specified shopping assistant.

        Parameters
        ----------
        shopping_assistant_id : str
            The unique identifier of the shopping assistant to be retrieved.
        account_id : Optional[str], optional
            The account ID to which the shopping assistant belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        ShoppingAssistant
            A ShoppingAssistant object containing the details of the specified assistant.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        shopping_assistant = (
            self.management_api.shopping_assistant_api.get_shopping_assistant(
                shopping_assistant_id=shopping_assistant_id,
                account_id=account_id or self.account_id,
            )
        )

        return ShoppingAssistant.model_validate(
            shopping_assistant.model_dump()
        )

    def create_shopping_assistant(
        self,
        name: Optional[str] = None,
        external_key: Optional[OpenAIKey] = None,
        llm_model_name: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> ShoppingAssistant:
        """
        Creates a new shopping assistant based on the provided details.

        Parameters
        ----------
        name: Optional[str], optional
            A string representing the name of the shopping assistant configuration.
            Must be unique based on account_id.
        external_key: Optional[OpenAIKey], optional
            Valid external key.
            This has to be OpenAI key for now.
        llm_model_name: Optional[str], optional
            A string representing the model name that the user wishes to use for the prompts.
            This has to be OpenAI model for now.
        account_id: Optional[str], optional
            The account ID to which the shopping assistant belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        ShoppingAssistant
            A ShoppingAssistant object representing the newly created shopping assistant.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """
        shopping_assistant_modifiable = ShoppingAssistantModifiable(
            name=name,
            external_account_id=external_key.external_key_id,
            llm_model_name=llm_model_name,
        )

        result = self.management_api.shopping_assistant_api.create_shopping_assistant(
            shopping_assistant_modifiable=shopping_assistant_modifiable,
            account_id=account_id or self.account_id,
        )

        return ShoppingAssistant.model_validate(result.model_dump())

    def update_shopping_assistant(
        self,
        shopping_assistant_id: str,
        name: Optional[str] = None,
        external_key: Optional[OpenAIKey] = None,
        llm_model_name: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> ShoppingAssistant:
        """
        Updates specified shopping assistant based on the provided parameters.

        Parameters
        ----------
        shopping_assistant_id: str
            The unique identifier of the shopping assistant to be updated.
        name: Optional[str], optional
            A string representing the name of the shopping assistant configuration.
            Must be unique based on account_id.
        external_key: Optional[OpenAIKey], optional
            Valid external key.
            This has to be OpenAI key for now.
        llm_model_name: Optional[str], optional
            A string representing the model name that the user wishes to use for the prompts.
            This has to be OpenAI model for now.
        account_id: Optional[str], optional
            The account ID to which the shopping assistant belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        ShoppingAssistant
            A ShoppingAssistant object representing the updated shopping assistant.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """
        shopping_assistant_modifiable = ShoppingAssistantModifiable(
            name=name,
            external_account_id=external_key.external_key_id,
            llm_model_name=llm_model_name,
        )

        result = self.management_api.shopping_assistant_api.update_shopping_assistant(
            shopping_assistant_id=shopping_assistant_id,
            shopping_assistant_modifiable=shopping_assistant_modifiable,
            account_id=account_id or self.account_id,
        )

        return ShoppingAssistant.model_validate(result.model_dump())

    def delete_shopping_assistant(
        self,
        shopping_assistant_id: str,
        account_id: Optional[str] = None,
    ) -> None:
        """
        Deletes a specific shopping assistant identified by its unique ID within a specified account.

        Parameters
        ----------
        shopping_assistant_id : str
            The unique identifier of the shopping assistant to be deleted.
        account_id : Optional[str], optional
            The account ID to which the shopping assistant belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        None

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        self.management_api.shopping_assistant_api.delete_shopping_assistant(
            shopping_assistant_id=shopping_assistant_id,
            account_id=account_id or self.account_id,
        )

    # endregion

    # region Vantage Vibe

    def list_vibe_configurations(
        self,
        account_id: Optional[str] = None,
    ) -> List[VantageVibe]:
        """
        Retrieves a list of Vantage vibe configurations associated with a given account.

        Parameters
        ----------
        account_id : Optional[str], optional
            The unique identifier of the account for which the vibe configurations are to be retrieved.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        List[VantageVibe]
            A list of VantageVibe objects.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        vantage_vibes = self.management_api.vantage_vibe_api.list_vantage_vibe(
            account_id=account_id or self.account_id,
        )

        return [
            VantageVibe.model_validate(vibe.model_dump())
            for vibe in vantage_vibes
        ]

    def get_vibe_configuration(
        self,
        vibe_id: str,
        account_id: Optional[str] = None,
    ) -> VantageVibe:
        """
        Retrieves the details of a specified Vantage vibe configuration.

        Parameters
        ----------
        vibe_id : str
            The unique identifier of the Vantage vibe configuration to be retrieved.
        account_id : Optional[str], optional
            The account ID to which the vibe configuration belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        VantageVibe
            A VantageVibe object containing the details of the specified vibe configuration.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        vibe = self.management_api.vantage_vibe_api.get_vantage_vibe(
            vibe_id=vibe_id,
            account_id=account_id or self.account_id,
        )

        return VantageVibe.model_validate(vibe.model_dump())

    def create_vibe_configuration(
        self,
        name: str,
        llm_model_name: str,
        external_key: Union[OpenAIKey, AnthropicKey],
        account_id: Optional[str] = None,
    ) -> VantageVibe:
        """
        Creates a new Vantage vibe configuration based on the provided parameters.

        Parameters
        ----------
        name: Optional[str], optional
            A string representing the name of the Vantage vibe configuration.
            Must be unique based on account_id.
        llm_model_name: Optional[str], optional
            A string representing the model name that the user wishes to use for the prompts.
            This has to be OpenAI or Anthropic model for now.
        external_key: Union[OpenAIKey, AnthropicKey]
            Valid external key.
            This has to be OpenAI or Anthropic key for now.
        account_id: Optional[str], optional
            The account ID to which the vibe configuration belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        VantageVibe
            A VantageVibe object representing the newly created vibe configuration.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        vibe_modifiable = VantageVibeModifiable(
            llm_model_name=llm_model_name,
            name=name,
            external_account_id=external_key.external_key_id,
        )

        result = self.management_api.vantage_vibe_api.create_vantage_vibe(
            vantage_vibe_modifiable=vibe_modifiable,
            account_id=account_id or self.account_id,
        )

        return VantageVibe.model_validate(result.model_dump())

    def update_vibe_configuration(
        self,
        vibe_id: str,
        name: Optional[str] = None,
        llm_model_name: Optional[str] = None,
        external_key: Optional[Union[OpenAIKey, AnthropicKey]] = None,
        account_id: Optional[str] = None,
    ) -> VantageVibe:
        """
        Updates specified Vantage vibe configuration based on the provided parameters.

        Parameters
        ----------
        vibe_id: str
            The unique identifier of the Vantage vibe to be updated.
        name: Optional[str], optional
            A string representing the name of the vibe configuration.
            Must be unique based on account_id.
        llm_model_name: Optional[str], optional
            A string representing the model name that the user wishes to use for the prompts.
            This has to be OpenAI model for now.
        external_key: Optional[Union[OpenAIKey, AnthropicKey]], optional
            Valid external key.
            This has to be OpenAI or Anthropic key for now.
        account_id: Optional[str], optional
            The account ID to which the vibe configuration belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        VantageVibe
            A VantageVibe object representing the updated vibe configuration.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        vibe_modifiable = VantageVibeModifiable(
            llm_model_name=llm_model_name,
            name=name,
            external_account_id=external_key.external_key_id,
        )

        result = self.management_api.vantage_vibe_api.update_vantage_vibe(
            vibe_id=vibe_id,
            vantage_vibe_modifiable=vibe_modifiable,
            account_id=account_id or self.account_id,
        )

        return VantageVibe.model_validate(result.model_dump())

    def delete_vibe_configuration(
        self,
        vibe_id: str,
        account_id: Optional[str] = None,
    ) -> None:
        """
        Deletes a specific vibe configuration identified by its unique ID within a specified account.

        Parameters
        ----------
        vibe_id : str
            The unique identifier of the Vantage vibe configuration to be deleted.
        account_id : Optional[str], optional
            The account ID to which the vibe configuration belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        None

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        self.management_api.vantage_vibe_api.delete_vantage_vibe(
            vibe_id=vibe_id,
            account_id=account_id or self.account_id,
        )

    # endregion

    # region Search Helper Functions

    def _prepare_search_query(
        self,
        accuracy: Optional[float] = None,
        pagination: Optional[Pagination] = None,
        filter: Optional[Filter] = None,
        sort: Optional[Sort] = None,
        field_value_weighting: Optional[FieldValueWeighting] = None,
        facets: Optional[List[Facet]] = None,
    ) -> SearchOptions:
        collection = (
            SearchOptionsCollection(
                accuracy=accuracy,
            )
            if accuracy
            else None
        )

        search_filter = (
            SearchOptionsFilter(
                boolean_filter=filter.boolean_filter,
                variant_filter=filter.variant_filter,
            )
            if filter
            else None
        )

        pagination = (
            SearchOptionsPagination(
                page=pagination.page,
                count=pagination.count,
                threshold=pagination.threshold,
            )
            if pagination
            else None
        )

        sort = (
            SearchOptionsSort(
                field=sort.field,
                order=sort.order,
                mode=sort.mode,
            )
            if sort
            else None
        )

        field_value_weighting = (
            SearchOptionsFieldValueWeighting(
                query_key_word_max_overall_weight=field_value_weighting.query_key_word_max_overall_weight,
                query_key_word_weighting_mode=field_value_weighting.query_key_word_weighting_mode,
                weighted_field_values=field_value_weighting.pydantic_weighted_field_values(),
            )
            if field_value_weighting
            else None
        )

        facets = (
            [
                SearchOptionsFacetsInner(
                    name=f.name,
                    type=f.type.value,
                    values=f.values,
                    ranges=[
                        pydantic_FacetRange(
                            value=range.value, min=range.min, max=range.max
                        )
                        for range in f.ranges
                    ],
                )
                for f in facets
            ]
            if facets
            else None
        )

        return SearchOptions(
            collection=collection,
            filter=search_filter,
            pagination=pagination,
            sort=sort,
            field_value_weighting=field_value_weighting,
            facets=facets,
        )

    def _vantage_api_key_check(self, vantage_api_key: str) -> str:
        vantage_api_key = (
            vantage_api_key if vantage_api_key else self.vantage_api_key
        )

        if not vantage_api_key:
            raise VantageValueError(
                "Vantage API Key is missing. Please provide the 'vantage_api_key' parameter to authenticate with the Search API."  # noqa: E501
            )

        return vantage_api_key

    # endregion

    # region Search

    def semantic_search(
        self,
        text: str,
        collection_id: str,
        accuracy: Optional[float] = None,
        pagination: Optional[Pagination] = None,
        filter: Optional[Filter] = None,
        sort: Optional[Sort] = None,
        field_value_weighting: Optional[FieldValueWeighting] = None,
        facets: Optional[List[Facet]] = None,
        total_counts: Optional[TotalCountsOptions] = None,
        vantage_api_key: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> SearchResult:
        """
        Performs a search within a specified collection using a text query
        and additional optional parameters.

        Check [Search Options](https://docs.vantagediscovery.com/docs/search-options)
        documentation page for more details.

        Parameters
        ----------
        text : str
            The text query for the semantic search.
        collection_id : str
            The ID of the collection to search within.
        accuracy : Optional[float], optional
            The accuracy threshold for the search.
            Defaults to None.
        pagination: Optional[Pagination], optional
            Pagination settings for the search results.
            Defaults to None.
        filter: Optional[Filter], optional
            Filter settings to narrow down the search results.
            Defaults to None.
        sort: Optional[Sort], optional
            Sorting settings for the search results.
            Defaults to None.
        field_value_weighting: Optional[FieldValueWeighting], optional
            Weighting settings for specific field values in the search.
            Defaults to None.
        facets: Optional[List[Facet]], optional
            Array of objects defining specific attributes of the data.
            Defaults to None.
        total_counts: Optional[TotalCountsOptions], optional
            Similarity score range used to calculate the total
            number of documents that match it.
        vantage_api_key : Optional[str], optional
            The Vantage API key used for authentication.
            If not provided, the instance's API key is used.
            Defaults to None.
        account_id : Optional[str], optional
            The account ID associated with the search.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        SearchResult
            An object containing the search results.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/search-api) for more details and examples.
        """

        vantage_api_key = self._vantage_api_key_check(vantage_api_key)

        search_properties = self._prepare_search_query(
            accuracy=accuracy,
            pagination=pagination,
            filter=filter,
            sort=sort,
            field_value_weighting=field_value_weighting,
            facets=facets,
        )

        query = SemanticSearchQuery(
            text=text,
            collection=search_properties.collection,
            filter=search_properties.filter,
            pagination=search_properties.pagination,
            sort=search_properties.sort,
            field_value_weighting=search_properties.field_value_weighting,
            facets=search_properties.facets,
            total_counts=(
                None if total_counts is None else total_counts.model_dump()
            ),
        )

        result = self.search_api.api.semantic_search(
            collection_id=collection_id,
            account_id=account_id or self.account_id,
            semantic_search_query=query,
            _headers={"authorization": f"Bearer {vantage_api_key}"},
        )

        return SearchResult.model_validate(result.model_dump())

    def embedding_search(
        self,
        embedding: List[float],
        collection_id: str,
        accuracy: Optional[float] = None,
        pagination: Optional[Pagination] = None,
        filter: Optional[Filter] = None,
        sort: Optional[Sort] = None,
        field_value_weighting: Optional[FieldValueWeighting] = None,
        facets: Optional[List[Facet]] = None,
        vantage_api_key: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> SearchResult:
        """
        Performs a search within a specified collection using an embedding vector and
        optional additional parameters.

        Check [Search Options](https://docs.vantagediscovery.com/docs/search-options)
        documentation page for more details.

        Parameters
        ----------
        embedding : List[int]
            The embedding vector used for the search.
        collection_id : str
            The ID of the collection to search within.
        accuracy : Optional[float], optional
            The accuracy threshold for the search.
            Defaults to None.
        pagination: Optional[Pagination], optional
            Pagination settings for the search results.
            Defaults to None.
        filter: Optional[Filter], optional
            Filter settings to narrow down the search results.
            Defaults to None.
        sort: Optional[Sort], optional
            Sorting settings for the search results.
            Defaults to None.
        field_value_weighting: Optional[FieldValueWeighting], optional
            Weighting settings for specific field values in the search.
            Defaults to None.
        facets: Optional[List[Facet]], optional
            Array of objects defining specific attributes of the data.
            Defaults to None.
        vantage_api_key : Optional[str], optional
            The Vantage API key used for authentication.
            If not provided, the instance's API key is used.
            Defaults to None.
        account_id : Optional[str], optional
            The account ID associated with the search.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        SearchResult
            An object containing the search results.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/search-api) for more details and examples.
        """

        vantage_api_key = self._vantage_api_key_check(vantage_api_key)

        search_properties = self._prepare_search_query(
            accuracy=accuracy,
            pagination=pagination,
            filter=filter,
            sort=sort,
            field_value_weighting=field_value_weighting,
            facets=facets,
        )

        query = EmbeddingSearchQuery(
            embedding=embedding,
            collection=search_properties.collection,
            filter=search_properties.filter,
            pagination=search_properties.pagination,
            sort=search_properties.sort,
            field_value_weighting=search_properties.field_value_weighting,
            facets=search_properties.facets,
        )

        result = self.search_api.api.embedding_search(
            collection_id=collection_id,
            account_id=account_id or self.account_id,
            embedding_search_query=query,
            _headers={"authorization": f"Bearer {vantage_api_key}"},
        )

        return SearchResult.model_validate(result.model_dump())

    def more_like_this_search(
        self,
        document_id: str,
        collection_id: str,
        accuracy: Optional[float] = None,
        pagination: Optional[Pagination] = None,
        filter: Optional[Filter] = None,
        sort: Optional[Sort] = None,
        field_value_weighting: Optional[FieldValueWeighting] = None,
        facets: Optional[List[Facet]] = None,
        account_id: Optional[str] = None,
        vantage_api_key: Optional[str] = None,
    ) -> SearchResult:
        """
        Performs a "More Like This" search to find documents similar to a specified
        document within a specified collection using optional additional parameters.

        Check [Search Options](https://docs.vantagediscovery.com/docs/search-options) and
        [More Like This](https://docs.vantagediscovery.com/docs/search-more-like-this)
        documentation pages for more details.

        Parameters
        ----------
        document_id : str
            The ID of the document to find similar documents to.
        collection_id : str
            The ID of the collection to search within.
        accuracy : Optional[float], optional
            The accuracy threshold for the search.
            Defaults to None.
        pagination: Optional[Pagination], optional
            Pagination settings for the search results.
            Defaults to None.
        filter: Optional[Filter], optional
            Filter settings to narrow down the search results.
            Defaults to None.
        sort: Optional[Sort], optional
            Sorting settings for the search results.
            Defaults to None.
        field_value_weighting: Optional[FieldValueWeighting], optional
            Weighting settings for specific field values in the search.
            Defaults to None.
        facets: Optional[List[Facet]], optional
            Array of objects defining specific attributes of the data.
            Defaults to None.
        vantage_api_key : Optional[str], optional
            The Vantage API key used for authentication.
            If not provided, the instance's API key is used.
            Defaults to None.
        account_id : Optional[str], optional
            The account ID associated with the search.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        SearchResult
            An object containing the search results similar to the specified document.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/search-api) for more details and examples.
        """

        vantage_api_key = self._vantage_api_key_check(vantage_api_key)

        search_properties = self._prepare_search_query(
            accuracy=accuracy,
            pagination=pagination,
            filter=filter,
            sort=sort,
            field_value_weighting=field_value_weighting,
            facets=facets,
        )

        query = MoreLikeThisQuery(
            document_id=document_id,
            collection=search_properties.collection,
            filter=search_properties.filter,
            pagination=search_properties.pagination,
            sort=search_properties.sort,
            field_value_weighting=search_properties.field_value_weighting,
            facets=search_properties.facets,
        )

        result = self.search_api.api.more_like_this_search(
            collection_id=collection_id,
            account_id=account_id or self.account_id,
            more_like_this_query=query,
            _headers={"authorization": f"Bearer {vantage_api_key}"},
        )

        return SearchResult.model_validate(result.model_dump())

    def more_like_these_search(
        self,
        more_like_these: list[MoreLikeTheseItem],
        collection_id: str,
        accuracy: Optional[float] = None,
        pagination: Optional[Pagination] = None,
        filter: Optional[Filter] = None,
        sort: Optional[Sort] = None,
        field_value_weighting: Optional[FieldValueWeighting] = None,
        facets: Optional[List[Facet]] = None,
        account_id: Optional[str] = None,
        vantage_api_key: Optional[str] = None,
    ) -> SearchResult:
        """
        Performs a "More Like These" search to find documents similar to a specified list
        of MoreLikeTheseItem objects within a specified collection using optional additional parameters.

        Check [Search Options](https://docs.vantagediscovery.com/docs/search-options)
        and [More Like These](https://docs.vantagediscovery.com/docs/search-more-like-these-tm)
        documentation pages for more details.

        Parameters
        ----------
        more_like_these : list[MoreLikeTheseItem]
            The list of "MoreLikeTheseItem" objects to find similar documents to.
        collection_id : str
            The ID of the collection to search within.
        accuracy : Optional[float], optional
            The accuracy threshold for the search.
            Defaults to None.
        pagination: Optional[Pagination], optional
            Pagination settings for the search results.
            Defaults to None.
        filter: Optional[Filter], optional
            Filter settings to narrow down the search results.
            Defaults to None.
        sort: Optional[Sort], optional
            Sorting settings for the search results.
            Defaults to None.
        field_value_weighting: Optional[FieldValueWeighting], optional
            Weighting settings for specific field values in the search.
            Defaults to None.
        facets: Optional[List[Facet]], optional
            Array of objects defining specific attributes of the data.
            Defaults to None.
        vantage_api_key : Optional[str], optional
            The Vantage API key used for authentication.
            If not provided, the instance's API key is used.
            Defaults to None.
        account_id : Optional[str], optional
            The account ID associated with the search.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        SearchResult
            An object containing the search results similar to the specified document.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/search-api) for more details and examples.
        """

        vantage_api_key = self._vantage_api_key_check(vantage_api_key)

        search_properties = self._prepare_search_query(
            accuracy=accuracy,
            pagination=pagination,
            filter=filter,
            sort=sort,
            field_value_weighting=field_value_weighting,
            facets=facets,
        )

        query = MoreLikeTheseQuery(
            these=[
                MLTheseTheseInner.model_validate(item.model_dump())
                for item in more_like_these
            ],
            collection=search_properties.collection,
            filter=search_properties.filter,
            pagination=search_properties.pagination,
            sort=search_properties.sort,
            field_value_weighting=search_properties.field_value_weighting,
            facets=search_properties.facets,
        )

        result = self.search_api.api.more_like_these_search(
            collection_id=collection_id,
            account_id=account_id or self.account_id,
            more_like_these_query=query,
            _headers={"authorization": f"Bearer {vantage_api_key}"},
        )

        return SearchResult.model_validate(result.model_dump())

    # endregion

    # region Search - Additional

    def vantage_vibe_search(
        self,
        collection_id: str,
        vibe_id: str,
        images: List[Union[VantageVibeImageUrl, VantageVibeImageBase64]],
        text: Optional[str],
        accuracy: Optional[float] = None,
        pagination: Optional[Pagination] = None,
        filter: Optional[Filter] = None,
        sort: Optional[Sort] = None,
        field_value_weighting: Optional[FieldValueWeighting] = None,
        facets: Optional[List[Facet]] = None,
        account_id: Optional[str] = None,
        vantage_api_key: Optional[str] = None,
    ) -> SearchResult:
        """
        Performs a Vantage Vibe search to find documents with the vibe similar to a specified list
        of image objects and text within a specified collection using optional additional parameters.

        Check [Search Options](https://docs.vantagediscovery.com/docs/search-options) and
        [Vantage Vibe](https://docs.vantagediscovery.com/docs/search-vantage-vibe)
        documentation pages for more details.

        Parameters
        ----------
        collection_id : str
            The ID of the collection to search within.
        vibe_id : str
            The ID of the Vantage vibe.
        images : list[Union[VantageVibeImageUrl, VantageVibeImageBase64]]
            The images to find documents with the same vibe.
        text: Optional[sting], optional
            The text query for the search.
        accuracy : Optional[float], optional
            The accuracy threshold for the search.
            Defaults to None.
        pagination: Optional[Pagination], optional
            Pagination settings for the search results.
            Defaults to None.
        filter: Optional[Filter], optional
            Filter settings to narrow down the search results.
            Defaults to None.
        sort: Optional[Sort], optional
            Sorting settings for the search results.
            Defaults to None.
        field_value_weighting: Optional[FieldValueWeighting], optional
            Weighting settings for specific field values in the search.
            Defaults to None.
        facets: Optional[List[Facet]], optional
            Array of objects defining specific attributes of the data.
            Defaults to None.
        vantage_api_key : Optional[str], optional
            The Vantage API key used for authentication.
            If not provided, the instance's API key is used.
            Defaults to None.
        account_id : Optional[str], optional
            The account ID associated with the search.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        SearchResult
            An object containing the search results similar to the specified document.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/search-api) for more details and examples.
        """

        if len(images) > 10 or len(images) < 1:
            raise VantageValueError(
                "The images array should contain at least one and up to 10 elements."
            )

        vantage_api_key = self._vantage_api_key_check(vantage_api_key)

        search_properties = self._prepare_search_query(
            accuracy=accuracy,
            pagination=pagination,
            filter=filter,
            sort=sort,
            field_value_weighting=field_value_weighting,
            facets=facets,
        )

        prepared_images = [
            VantageVibeImage(
                url=image.url,
                image=image.base64,
            )
            for image in images
        ]

        vantage_vibe_search_query = VantageVibeSearchQuery(
            vibe_id=vibe_id,
            text=text,
            images=prepared_images,
            collection=search_properties.collection,
            filter=search_properties.filter,
            pagination=search_properties.pagination,
            sort=search_properties.sort,
            field_value_weighting=search_properties.field_value_weighting,
            facets=search_properties.facets,
        )

        result = self.search_api.api.vantage_vibe_search(
            collection_id=collection_id,
            account_id=account_id or self.account_id,
            vantage_vibe_search_query=vantage_vibe_search_query,
            _headers={"authorization": f"Bearer {vantage_api_key}"},
        )

        return SearchResult.model_validate(result.model_dump())

    def shopping_assistant_search(
        self,
        collection_id: str,
        text: str,
        shopping_assistant_id: str,
        max_groups: Optional[int] = 5,
        accuracy: Optional[float] = None,
        pagination: Optional[Pagination] = None,
        filter: Optional[Filter] = None,
        sort: Optional[Sort] = None,
        field_value_weighting: Optional[FieldValueWeighting] = None,
        facets: Optional[List[Facet]] = None,
        account_id: Optional[str] = None,
        vantage_api_key: Optional[str] = None,
    ) -> ShoppingAssistantResult:
        """
        Performs a search using a help of shopping assistant to find documents
        within a specified collection and optional additional parameters.

        Check [Search Options](https://docs.vantagediscovery.com/docs/search-options)
        and [ShoppingAssistant](https://docs.vantagediscovery.com/docs/search-shopping-assistant)
        documentation pages for more details.

        Parameters
        ----------
        collection_id : str
            The ID of the collection to search within.
        text: str
            Query for the LLM to parse into groups based on the predefined system prompt.
        shopping_assistant_id: str
            The ID of the shopping assistant configuration linked to specified collection.
        max_groups: Optional[int], optional
            Max number of groups the user wants to give back.
            Defaults to 5.
        accuracy : Optional[float], optional
            The accuracy threshold for the search.
            Defaults to None.
        pagination: Optional[Pagination], optional
            Pagination settings for the search results.
            Defaults to None.
        filter: Optional[Filter], optional
            Filter settings to narrow down the search results.
            Defaults to None.
        sort: Optional[Sort], optional
            Sorting settings for the search results.
            Defaults to None.
        field_value_weighting: Optional[FieldValueWeighting], optional
            Weighting settings for specific field values in the search.
            Defaults to None.
        facets: Optional[List[Facet]], optional
            Array of objects defining specific attributes of the data.
            Defaults to None.
        vantage_api_key : Optional[str], optional
            The Vantage API key used for authentication.
            If not provided, the instance's API key is used.
            Defaults to None.
        account_id : Optional[str], optional
            The account ID associated with the search.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        ShoppingAssistantResult
            An object containing the search results, grouped as configured in the shopping assistant.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/search-api) for more details and examples.
        """
        vantage_api_key = self._vantage_api_key_check(vantage_api_key)

        search_properties = self._prepare_search_query(
            accuracy=accuracy,
            pagination=pagination,
            filter=filter,
            sort=sort,
            field_value_weighting=field_value_weighting,
            facets=facets,
        )

        query = ShoppingAssistantQuery(
            text=text,
            max_groups=max_groups,
            shopping_assistant_id=shopping_assistant_id,
            collection=search_properties.collection,
            filter=search_properties.filter,
            pagination=search_properties.pagination,
            sort=search_properties.sort,
            field_value_weighting=search_properties.field_value_weighting,
            facets=search_properties.facets,
        )

        result = self.search_api.api.shopping_assistant(
            collection_id=collection_id,
            account_id=account_id or self.account_id,
            shopping_assistant_query=query,
            _headers={"authorization": f"Bearer {vantage_api_key}"},
        )

        return ShoppingAssistantResult.model_validate(result.model_dump())

    def approximate_results_count_search(
        self,
        text: str,
        collection_id: str,
        total_counts: TotalCountsOptions,
        accuracy: Optional[float] = None,
        pagination: Optional[Pagination] = None,
        filter: Optional[Filter] = None,
        sort: Optional[Sort] = None,
        field_value_weighting: Optional[FieldValueWeighting] = None,
        facets: Optional[List[Facet]] = None,
        vantage_api_key: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> ApproximateResultsCountResult:
        """
        Performs a search within a specified collection using a text query and
        optional additional parameters.

        Check [Search Options](https://docs.vantagediscovery.com/docs/search-options) and
        [Approximate Results Count Search](https://docs.vantagediscovery.com/docs/search-approximate-results-count)
        documentation pages for more details.

        Parameters
        ----------
        text : str
            The text query for the semantic search.
        collection_id : str
            The ID of the collection to search within.
        total_counts: TotalCountsOptions
            Similarity score range used to calculate the total
            number of documents that match it.
        accuracy : Optional[float], optional
            The accuracy threshold for the search.
            Defaults to None.
        pagination: Optional[Pagination], optional
            Pagination settings for the search results.
            Defaults to None.
        filter: Optional[Filter], optional
            Filter settings to narrow down the search results.
            Defaults to None.
        sort: Optional[Sort], optional
            Sorting settings for the search results.
            Defaults to None.
        field_value_weighting: Optional[FieldValueWeighting], optional
            Weighting settings for specific field values in the search.
            Defaults to None.
        facets: Optional[List[Facet]], optional
            Array of objects defining specific attributes of the data.
            Defaults to None.
        vantage_api_key : Optional[str], optional
            The Vantage API key used for authentication.
            If not provided, the instance's API key is used.
            Defaults to None.
        account_id : Optional[str], optional
            The account ID associated with the search.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        ApproximateResultsCountResult
            An object containing the total count of documents that
            match total_counts threshold range.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/search-api) for more details and examples.
        """

        vantage_api_key = self._vantage_api_key_check(vantage_api_key)

        search_properties = self._prepare_search_query(
            accuracy=accuracy,
            pagination=pagination,
            filter=filter,
            sort=sort,
            field_value_weighting=field_value_weighting,
            facets=facets,
        )

        query = SemanticSearchQuery(
            text=text,
            collection=search_properties.collection,
            filter=search_properties.filter,
            pagination=search_properties.pagination,
            sort=search_properties.sort,
            field_value_weighting=search_properties.field_value_weighting,
            facets=search_properties.facets,
            total_counts=total_counts.model_dump(),
        )

        result = self.search_api.api.approximate_results_count_search(
            collection_id=collection_id,
            account_id=account_id or self.account_id,
            semantic_search_query=query,
            _headers={"authorization": f"Bearer {vantage_api_key}"},
        )

        return TotalCountResult.model_validate(result.model_dump())

    # endregion

    # region Documents - Upsert Helper Functions

    def _document_to_collection_compatibility_check(
        self,
        collection: Collection,
        document: Union[
            UserProvidedEmbeddingsDocument, VantageManagedEmbeddingsDocument
        ],
    ) -> None:
        """
        Checks if a document is compatible with the type of the specified collection.

        Parameters
        ----------
        collection : Collection
            The collection to which the document is intended to be added. This object should specify whether it
            expects user-provided embeddings or Vantage-managed embeddings.
        document : Union[UserProvidedEmbeddingsDocument, VantageManagedEmbeddingsDocument]
            The document to be checked for compatibility with the collection. This must be an instance of either
            UserProvidedEmbeddingsDocument or VantageManagedEmbeddingsDocument.
        """
        if collection.user_provided_embeddings and isinstance(
            document, VantageManagedEmbeddingsDocument
        ):
            raise ValueError(
                f"Embeddings are required for User-provided embeddings collection. Please provide a list of {UserProvidedEmbeddingsDocument.__name__} objects."  # noqa: E501
            )
        elif not collection.user_provided_embeddings and isinstance(
            document, UserProvidedEmbeddingsDocument
        ):
            raise ValueError(
                f"Embeddings are not required for Vantage-managed embeddings collection. Please provide a list of {VantageManagedEmbeddingsDocument.__name__} objects."  # noqa: E501
            )

    def _upload_documents_using_direct_upload_url(
        self,
        direct_upload_url: str,
        upload_content,
    ) -> int:
        """
        Uploads content to a specified collection using a direct upload URL.

        Parameters
        ----------
        direct_upload_url : str
            The URL to which the content should be uploaded. This URL should be pre-configured to
            accept uploads for a specific collection.
        upload_content
            The content to be uploaded.

        Returns
        -------
        int
            The HTTP status code returned by the server after attempting the upload.
        """
        response = requests.put(
            direct_upload_url,
            data=upload_content,
        )

        if response.status_code != 200:
            raise VantageFileUploadError(response.reason, response.status_code)

        return response.status_code

    def _upload_documents_from_bytes(
        self,
        collection_id: str,
        content: bytes,
        file_size: int,
        batch_identifier: Optional[str],
        account_id: Optional[str] = None,
    ) -> int:
        """
        Upserts documents as bytes to a collection.

        Parameters
        ----------
        collection_id : str
            The identifier of the collection to which the documents are being upserted.
        content : bytes
            The binary content (documents in bytes) to be uploaded.
        file_size : int
            The size of the content to be uploaded, in bytes.
        batch_identifier : Optional[str], optional
            An optional identifier for the batch upload. If not provided, a unique identifier is generated.
            If provided without a '.parquet' extension, it will be appended. Defaults to None.
        account_id : Optional[str], optional
            The account identifier under which the collection exists. If not provided, the default account
            associated with the user is used. Defaults to None.

        Returns
        -------
        int
            The HTTP status code returned by the server after attempting the upload.
        """

        if batch_identifier is None:
            batch_identifier = f"{uuid.uuid4}.parquet"
        elif not (
            batch_identifier.endswith(".parquet")
            or batch_identifier.endswith(".jsonl")
        ):
            # Add ".parquet" extension to batch identifier,
            # so the document ingestion step won't ignore it.
            batch_identifier = f"{batch_identifier}.parquet"

        direct_upload_url = self._get_direct_upload_url(
            collection_id=collection_id,
            file_size=file_size,
            parquet_file_name=batch_identifier,
            account_id=account_id,
        )

        return self._upload_documents_using_direct_upload_url(
            direct_upload_url=direct_upload_url.upload_url,
            upload_content=content,
        )

    # endregion

    # region Documents - Upsert

    def upsert_documents(
        self,
        collection_id: str,
        documents: Union[
            List[VantageManagedEmbeddingsDocument],
            List[UserProvidedEmbeddingsDocument],
        ],
        account_id: Optional[str] = None,
    ):
        """
        Upserts documents to a specified collection from a list of Vantage
        documents. The `documents` object should be a list of one type of Vantage
        document objects—either VantageManagedEmbeddingsDocument or UserProvidedEmbeddingsDocument,
        depending on the type of the collection to which you are upserting.

        Parameters
        ----------
        collection_id : str
            The unique identifier for the collection to which the documents will be upserted.
        documents : Union[List[VantageManagedEmbeddingsDocument], List[UserProvidedEmbeddingsDocument]]
            A list of documents to upsert. This list should contain only one type of document,
            either VantageManagedEmbeddingsDocument or UserProvidedEmbeddingsDocument,
            depending on the collection's type.
        account_id : Optional[str], optional
            The account ID to which the collection belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.


        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """
        if not documents:
            raise ValueError("Documents object can't be empty.")

        collection = self.get_collection(
            collection_id=collection_id,
            account_id=account_id or self.account_id,
        )

        self._document_to_collection_compatibility_check(
            collection=collection,
            document=documents[0],
        )

        vantage_documents_jsonl = "\n".join(
            map(
                json.dumps,
                [document.to_vantage_dict() for document in documents],
            )
        )

        self.upsert_documents_from_jsonl_string(
            collection_id=collection_id,
            documents_jsonl=vantage_documents_jsonl,
            account_id=account_id or self.account_id,
        )

    def upsert_documents_from_jsonl_string(
        self,
        collection_id: str,
        documents_jsonl: str,
        batch_identifier: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> None:
        """
        Upserts documents to a specified collection from a string containing JSONL-formatted documents.
        The `documents` string is expected to be in JSONL format, where each line is a valid JSON
        document.

        Parameters
        ----------
        collection_id : str
            The unique identifier of the collection to which the documents will be uploaded.
        documents_jsonl : str
            A string containing the documents to be uploaded, formatted as JSONL.
        batch_identifier : Optional[str], optional
            An optional identifier provided by the user to track the batch of document uploads.
        account_id : Optional[str], optional
            The account ID to which the collection belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        lines_count = count_lines(documents_jsonl)

        if lines_count <= _DOCUMENTS_UPLOAD_BATCH_SIZE:
            self.management_api.documents_api.upload_documents(
                body=documents_jsonl,
                account_id=account_id if account_id else self.account_id,
                collection_id=collection_id,
                customer_batch_identifier=batch_identifier,
            )
            return

        splitter = TextSplitter(
            text=documents_jsonl,
            batch_size=_DOCUMENTS_UPLOAD_BATCH_SIZE,
        )
        for batch in splitter.batch():
            batch.strip()

            if str.isspace(batch):
                continue

            self.management_api.documents_api.upload_documents(
                body=batch,
                account_id=account_id if account_id else self.account_id,
                collection_id=collection_id,
                customer_batch_identifier=batch_identifier,
            )

    def upsert_documents_from_jsonl_file(
        self,
        collection_id: str,
        jsonl_file_path: str,
        batch_identifier: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> None:
        """
        Upserts documents to a specified collection from a JSONL file located at a given file path.
        This method checks if the file exists at the specified path and raises a FileNotFoundError if it does not.
        It then reads the file and uploads the documents contained within the file to the specified
        collection using the `upsert_documents_from_jsonl_string` method.

        Parameters
        ----------
        collection_id : str
            The unique identifier of the collection to which the documents will be uploaded.
        file_path : str
            The path to the JSONL file containing the documents to be uploaded.
        batch_identifier : Optional[str], optional
            An optional identifier provided by the user to track the batch of document uploads.
        account_id : Optional[str], optional
            The account ID to which the collection belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        if not exists(jsonl_file_path):
            raise FileNotFoundError(f"File \"{jsonl_file_path}\" not found.")

        with BatchTextFileReader(
            file_path=jsonl_file_path,
            batch_size=_DOCUMENTS_UPLOAD_BATCH_SIZE,
        ) as reader:
            while True:
                batch = reader.next()

                if not any(batch):
                    return

                self.upsert_documents_from_jsonl_string(
                    collection_id=collection_id,
                    documents_jsonl=batch,
                    batch_identifier=batch_identifier,
                    account_id=account_id,
                )

    # endregion

    # region Documents - Delete

    def delete_documents(
        self,
        collection_id: str,
        document_ids: List[str],
        account_id: Optional[str] = None,
    ) -> None:
        """
        Deletes a list of documents from a specified collection.

        Parameters
        ----------
        collection_id : str
            The unique identifier of the collection from which documents are to be deleted.
        document_ids : List[str]
            A list of document IDs that need to be deleted from the collection.
        account_id : Optional[str], optional
            The account identifier under which the collection exists.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        documents_to_delete = [
            {"id": id, "operation": "delete"} for id in document_ids
        ]

        vantage_documents_jsonl = "\n".join(
            map(
                json.dumps,
                [document for document in documents_to_delete],
            )
        )

        self.upsert_documents_from_jsonl_string(
            collection_id=collection_id,
            documents_jsonl=vantage_documents_jsonl,
            account_id=account_id or self.account_id,
        )

    # endregion

    # region Documents - Upload File

    def upload_documents_from_parquet_file(
        self,
        collection_id: str,
        parquet_file_path: str,
        account_id: Optional[str] = None,
    ) -> int:
        """
        Uploads documents from a parquet file to a collection.

        Parameters
        ----------
        collection_id : str
            The unique identifier of the collection
            embeddings are being uploaded to.
        parquet_file_path : str
            Path to the parquet file in a filesystem.
        account_id : Optional[str], optional
            The account ID to which the collection belongs.
            If not provided, the instance's account ID is used.
            Defaults to None

        Returns
        -------
        int
            HTTP status of upload execution.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """

        if not exists(parquet_file_path):
            raise FileNotFoundError(f"File \"{parquet_file_path}\" not found.")

        file_name = ntpath.basename(parquet_file_path)
        file_type = magic.from_file(parquet_file_path)
        batch_identifier = file_name

        if file_type != _PARQUET_FILE_TYPE:
            raise ValueError("File must be a valid parquet file.")

        if not batch_identifier.endswith(".parquet"):
            batch_identifier = f"{batch_identifier}.parquet"

        file_size = Path(parquet_file_path).stat().st_size
        file = open(parquet_file_path, "rb")
        file_content = file.read()
        return self._upload_documents_from_bytes(
            collection_id=collection_id,
            content=file_content,
            file_size=file_size,
            batch_identifier=file_name,
            account_id=account_id,
        )

    def upload_documents_from_jsonl_file(
        self,
        collection_id: str,
        jsonl_file_path: str,
        account_id: Optional[str] = None,
    ) -> int:
        """
        Uploads documents from a parquet file to a collection.

        Parameters
        ----------
        collection_id : str
            The unique identifier of the collection
            embeddings are being uploaded to.
        jsonl_file_path : str
            Path to the JSONL file in a filesystem.
        account_id : Optional[str], optional
            The account ID to which the collection belongs.
            If not provided, the instance's account ID is used.
            Defaults to None

        Returns
        -------
        int
            HTTP status of upload execution.

        Notes
        -----
        Visit our [documentation](https://docs.vantagediscovery.com/docs/management-api) for more details and examples.
        """
        if not exists(jsonl_file_path):
            raise FileNotFoundError(f"File \"{jsonl_file_path}\" not found.")

        file_name = ntpath.basename(jsonl_file_path)
        mime_type = magic.from_file(jsonl_file_path, mime=True)
        batch_identifier = file_name

        # On some systems, magic identifies JSONL data as JSON data.
        if mime_type not in (_JSONL_MIME_TYPE, _JSON_MIME_TYPE):
            raise ValueError("File must be a valid JSONL file")

        if not batch_identifier.endswith(".jsonl"):
            batch_identifier = f"{batch_identifier}.jsonl"

        file_size = Path(jsonl_file_path).stat().st_size
        file = open(jsonl_file_path, "rb")
        file_content = file.read()

        return self._upload_documents_from_bytes(
            collection_id=collection_id,
            content=file_content,
            file_size=file_size,
            batch_identifier=file_name,
            account_id=account_id,
        )

    # endregion

    # region Documents - Validate File

    def validate_documents_from_jsonl(
        self,
        file_path: str,
        collection_type: CollectionType,
        model: Optional[str] = None,
        embeddings_dimension: Optional[int] = None,
    ) -> list[ValidationError]:
        """
        Validates documents from a JSONL file.

        Parameters
        ----------
        file_path : str
            Path of the JSONL file in the filesystem.
        collection_type : CollectionType
            For what kind of collection are documents from this file intended.
        model : Optional[str] = None
            Which model should be used to generate embeddings (if any).
        embeddings_dimension : Optional[int] = None
            Dimension of embeddings (if provided in file).

        Raises
        ------
        FileNotFoundError
            If specified file is not found.

        Returns
        -------
        List of encountered errors. If file is valid, the list will be empty.
        """

        return validator.validate_jsonl(
            file_path=file_path,
            collection_type=collection_type,
            model=model,
            embeddings_dimension=embeddings_dimension,
        )

    def validate_documents_from_parquet(
        self,
        file_path: str,
        collection_type: CollectionType,
        model: Optional[str] = None,
        embeddings_dimension: Optional[int] = None,
    ) -> list[ValidationError]:
        """
        Validates documents from a Parquet file.

        Parameters
        ----------
        file_path : str
            Path of the Parquet file in the filesystem.
        collection_type : CollectionType
            For what kind of collection are documents from this file intended.
        model : Optional[str] = None
            Which model should be used to generate embeddings (if any).
        embeddings_dimension : Optional[int] = None
            Dimension of embeddings (if provided in file).

        Raises
        ------
        FileNotFoundError
            If specified file is not found.

        Returns
        -------
        List of encountered errors. If file is valid, the list will be empty.
        """

        return validator.validate_parquet(
            file_path=file_path,
            collection_type=collection_type,
            model=model,
            embeddings_dimension=embeddings_dimension,
        )

    # endregion
