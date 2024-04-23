from __future__ import annotations

import ntpath
import uuid
import json
from os.path import exists
from pathlib import Path
from typing import List, Optional, Union

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
    CreateCollectionRequest,
    SecondaryExternalAccount as OpenAPISecondaryExternalAccount,
    CollectionModifiableSecondaryExternalAccountsInner,
    EmbeddingSearchQuery,
    ExternalAPIKeyModifiable,
    GlobalSearchPropertiesCollection,
    GlobalSearchPropertiesFilter,
    GlobalSearchPropertiesPagination,
    GlobalSearchPropertiesSort,
    MLTheseTheseInner,
    MoreLikeTheseQuery,
    MoreLikeThisQuery,
    SemanticSearchQuery,
)
from vantage_sdk.core.management import ManagementAPI
from vantage_sdk.core.search import SearchAPI
from vantage_sdk.exceptions import VantageFileUploadError, VantageValueError
from vantage_sdk.model.account import Account
from vantage_sdk.model.collection import (
    Collection,
    CollectionUploadURL,
    UserProvidedEmbeddingsCollection,
    OpenAICollection,
    HuggingFaceCollection,
)
from vantage_sdk.model.keys import (
    ExternalAPIKey,
    SecondaryExternalAccount,
    LLMProvider,
    VantageAPIKey,
)
from vantage_sdk.model.search import (
    GlobalSearchProperties,
    MoreLikeTheseItem,
    SearchResult,
)
from vantage_sdk.model.document import (
    VantageManagedEmbeddingsDocument,
    UserProvidedEmbeddingsDocument,
    MetadataItem,
)


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
        Initializes a new instance of the 'VantageClient' class, the main
        entry point for interacting with Vantage Discovery via the Python SDK,
        setting up the necessary APIs for management and search operations.

        Parameters
        ----------
        management_api : ManagementAPI
            An instance of the ManagementAPI class to manage accounts, collections and keys.
        search_api : SearchAPI
            An instance of the SearchAPI class to perform search operations.
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
        Instantiates a `VantageClient` using a Vantage API key for authentication.

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
        host = f"{api_host}/{API_HOST_VERSION}"

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
        Instantiates a `VantageClient` using a JWT token for authentication.

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
        Instantiates a `VantageClient` using OAuth client credentials for authentication.

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
        Retrieves the details of an Account.

        This method fetches the details of an account identified by its account ID.
        If the account ID is not specified, it defaults to the account ID of the current instance.
        It uses the Management API to retrieve the account information and returns an Account object upon success.

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

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> account = vantage_client.get_account()
        >>> print(account.name)
        "Example Account Name"
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
        Updates the Account.

        This method allows for updating the name of an account identified by its account ID.
        If the account ID is not specified, it defaults to the account ID of the current instance.
        It uses the Management API to perform the update operation and returns an updated Account object upon success.

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

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> updated_account = vantage_client.update_account(account_name="New Account Name")
        >>> print(updated_account.name)
        "New Account Name"
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

        This method fetches all the Vantage API keys associated with an account identified by its account ID.
        If the account ID is not specified, it defaults to the account ID of the current instance.
        It uses the Management API to retrieve the keys and returns a list of VantageAPIKey objects upon success.

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

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> vantage_api_keys = vantage_client.get_vantage_api_keys()
        >>> for key in vantage_api_keys:
        ...     print(key.value)
        "12345"
        "54321"
        """

        keys = self.management_api.vantage_api_keys_api.get_vantage_api_keys(
            account_id=account_id or self.account_id,
        )

        return [
            VantageAPIKey.model_validate(key.actual_instance.model_dump())
            for key in keys
        ]

    def get_vantage_api_key(
        self,
        vantage_api_key_id: str,
        account_id: Optional[str] = None,
    ) -> VantageAPIKey:
        """
        Retrieves a specific Vantage API key for a given account.

        This method obtains the details of a specific Vantage API key identified
        by `vantage_api_key_id` for the account specified by `account_id`.
        If the account ID is not specified, it defaults to the account ID of the current instance.
        It uses the Management API to retrieve the key and returns an VantageAPIKey object upon success.

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

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> vantage_api_key = vantage_client.get_vantage_api_key(vantage_api_key_id="api_key_12345")
        >>> print(vantage_api_key.value)
        "12345"
        """

        key = self.management_api.vantage_api_keys_api.get_vantage_api_key(
            account_id=account_id or self.account_id,
            vantage_api_key_id=vantage_api_key_id,
        )
        return VantageAPIKey.model_validate(key.model_dump())

    # endregion

    # region External API keys

    def get_external_api_keys(
        self,
        account_id: Optional[str] = None,
    ) -> List[ExternalAPIKey]:
        """
        Retrieves a list of external API keys associated with a given account.

        This method fetches all external API keys linked to the account specified by `account_id`.
        If `account_id` is not provided, it defaults to the account ID of the current instance.
        It uses the Management API to obtain the keys and returns a list of ExternalAPIKey objects upon success.

        Parameters
        ----------
        account_id : Optional[str], optional
            The unique identifier of the account for which the external API keys are to be retrieved.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        List[ExternalAPIKey]
            A list of ExternalAPIKey objects, each representing an external API key associated with the account.

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> external_api_keys = vantage_client.get_external_api_keys()
        >>> for key in external_api_keys:
        ...     print(key.id)
        "external_key_123"
        "external_key_321"
        """

        keys = self.management_api.external_api_keys_api.get_external_api_keys(
            account_id=account_id or self.account_id,
        )
        return [
            ExternalAPIKey.model_validate(key.actual_instance.model_dump())
            for key in keys
        ]

    def get_external_api_key(
        self,
        external_key_id: str,
        account_id: Optional[str] = None,
    ) -> ExternalAPIKey:
        """
        Retrieves a specific external API key associated with a given account.

        This method fetches the details of an external API key identified
        by `external_key_id` for the account specified by `account_id`.
        If `account_id` is not provided, it defaults to the account ID of the current instance.
        It uses the Management API to perform the retrieval and returns an ExternalAPIKey
        object containing the details of the requested API key upon success.

        Parameters
        ----------
        external_key_id : str
            The unique identifier of the external API key to be retrieved.
        account_id : Optional[str], optional
            The unique identifier of the account to which the external API key is associated.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        ExternalAPIKey
            An ExternalAPIKey object containing the details of the requested external API key.

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> external_api_key = vantage_client.get_external_api_key(external_key_id="external_key_123")
        >>> print(external_api_key.llm_provider)
        "OpenAI"
        """

        key = self.management_api.external_api_keys_api.get_external_api_key(
            account_id=account_id or self.account_id,
            external_key_id=external_key_id,
        )

        return ExternalAPIKey.model_validate(key.model_dump())

    def create_external_api_key(
        self,
        llm_provider: str,
        llm_secret: str,
        account_id: Optional[str] = None,
    ) -> ExternalAPIKey:
        """
        Creates a new external API key associated with a given account.

        This method generates a new external API key for integrating with external services, specified by the
        URL, LLM (Large Language Model) provider, and a secret for the LLM.
        The API key is associated with the account identified by `account_id`.
        If `account_id` is not provided, it defaults to the account ID of the current instance.
        It uses the Management API for the creation operation and returns an ExternalAPIKey object upon success.

        Parameters
        ----------
        llm_provider : str
            The provider of the Large Language Model (LLM).
            Supported options are: OpenAI and HuggingFace (Hugging)
        llm_secret : str
            The secret key for accessing the LLM.
        account_id : Optional[str], optional
            The unique identifier of the account for which the external API key is to be created.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        ExternalAPIKey
            An ExternalAPIKey object containing the details of the newly created API key.

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> external_api_key = vantage_client.create_external_api_key(
        ...     llm_provider="OpenAI",
        ...     llm_secret="secret123",
        ... )
        >>> print(external_api_key.id)
        "external_key_123"
        """

        external_api_key_modifiable = ExternalAPIKeyModifiable(
            llm_provider=llm_provider, llm_secret=llm_secret
        )

        key = (
            self.management_api.external_api_keys_api.create_external_api_key(
                account_id=account_id or self.account_id,
                external_api_key_modifiable=external_api_key_modifiable,
            )
        )

        return ExternalAPIKey.model_validate(key.model_dump())

    def update_external_api_key(
        self,
        external_key_id: str,
        llm_provider: str,
        llm_secret: str,
        account_id: Optional[str] = None,
    ) -> ExternalAPIKey:
        """
        Updates the details of a specific external API key associated with a given account.

        This method allows for updating the URL, LLM (Large Language Model) provider, and LLM secret of an
        external API key identified by `external_key_id`.
        If `account_id` is not specified, it defaults to using the account ID of the current instance.
        It uses the Management API to perform the update and returns an updated ExternalAPIKey object upon success.

        Parameters
        ----------
        external_key_id : str
            The unique identifier of the external API key to be updated.
        llm_provider : str
            The new provider of the Large Language Model (LLM).
        llm_secret : str
            The new secret key for accessing the LLM.
        account_id : Optional[str], optional
            The unique identifier of the account to which the external API key is associated.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        ExternalAPIKey
            An ExternalAPIKey object containing the updated details of the external API key.

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> updated_external_api_key = vantage_client.update_external_api_key(
        ...     external_key_id="external_key_123",
        ...     llm_provider="OpenAI",
        ...     llm_secret="new_secret_123",
        ... )
        >>> print(updated_external_api_key.llm_secret)
        "new_secret_123"
        """

        external_api_key_modifiable = ExternalAPIKeyModifiable(
            llm_provider=llm_provider, llm_secret=llm_secret
        )

        key = (
            self.management_api.external_api_keys_api.update_external_api_key(
                account_id=account_id or self.account_id,
                external_key_id=external_key_id,
                external_api_key_modifiable=external_api_key_modifiable,
            )
        )

        return ExternalAPIKey.model_validate(key.model_dump())

    def delete_external_api_key(
        self,
        external_key_id: str,
        account_id: Optional[str] = None,
    ) -> None:
        """
        Deletes a specific external API key associated with a given account.

        This method removes an external API key identified by `external_key_id`
        from the account specified by `account_id`.
        If `account_id` is not provided, it defaults to the account ID of the current instance.
        It uses the Management API to perform the deletion.

        Parameters
        ----------
        external_key_id : str
            The unique identifier of the external API key to be deleted.
        account_id : Optional[str], optional
            The unique identifier of the account to which the external API key is associated.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> vantage_client.delete_external_api_key(external_key_id="external_key_123")
        """

        self.management_api.external_api_keys_api.delete_external_api_key(
            account_id=account_id or self.account_id,
            external_key_id=external_key_id,
        )

    # endregion

    # region Collections

    def _existing_collection_ids(
        self,
        account_id: Optional[str] = None,
    ) -> List[str]:
        """
        Retrieves a list of existing collection IDs associated with a given account.

        This private method fetches the IDs of all collections linked to the account specified by `account_id`.
        If `account_id` is not provided, it defaults to the account ID of the current instance.

        Parameters
        ----------
        account_id : Optional[str], optional
            The unique identifier of the account for which the collection IDs are to be retrieved.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        List[str]
            A list of strings, each representing the unique ID of a collection associated with the account.
        """

        collections = self.list_collections(
            account_id=account_id or self.account_id
        )
        return [col.model_dump()["collection_id"] for col in collections]

    def _get_browser_upload_url(
        self,
        collection_id: str,
        file_size: int,
        parquet_file_name: str,
        account_id: Optional[str] = None,
    ) -> CollectionUploadURL:
        """
        Retrieves a browser upload URL for uploading files to a specified collection.
        It verifies the existence of the collection within the specified account and
        raises an exception if the collection does not exist.
        The method generates a URL that can be used to upload files directly from a browser,
        using specified file sizes and an optional customer batch identifier for tracking.

        Parameters
        ----------
        collection_id : str
            The unique identifier of the collection to which the file will be uploaded.
        file_size : int
            The size of the file to be uploaded, in bytes.
        parquet_file_name : str
            Name of the parquet file being uploaded.
        account_id : Optional[str], optional
            The account ID to which the collection belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        CollectionUploadURL
            An object containing the URL for browser-based file uploads.
        """

        url = self.management_api.collection_api.get_browser_upload_url(
            collection_id=collection_id,
            file_size=file_size,
            customer_batch_identifier=parquet_file_name,
            account_id=account_id or self.account_id,
        )

        return CollectionUploadURL.model_validate(url.model_dump())

    def list_collections(
        self,
        account_id: Optional[str] = None,
    ) -> List[Collection]:
        """
        Retrieves a list of collections associated with a given account.

        This method fetches all collections linked to the account specified by `account_id`.
        If `account_id` is not provided, it defaults to the account ID of the current instance.
        It uses the Management API to obtain the list of collections and
        returns a list of Collection objects upon success.

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

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> collections = vantage_client.list_collections(account_id="12345")
        >>> for collection in collections:
        ...     print(collection.name)
        "Collection 1"
        "Collection 2"
        """

        collections = self.management_api.collection_api.list_collections(
            account_id=account_id or self.account_id
        )

        return [
            Collection.model_validate(collection.actual_instance.model_dump())
            for collection in collections
        ]

    def get_collection(
        self,
        collection_id: str,
        account_id: Optional[str] = None,
    ) -> Collection:
        """
        Retrieves the details of a specified collection.

        This method fetches the details of a collection identified
        by its unique ID within a specified account.
        It checks for the existence of the collection ID and raises
        an exception if no collection with the given ID exists.
        The method returns a Collection object containing
        the collection's details upon successful retrieval.

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

        Example
        -------
        >>> vantage_client = VantageClient()
        >>> collection = vantage_client.get_collection(collection_id="unique_collection_id")
        >>> print(collection.name)
        "My Collection"
        """

        collection = self.management_api.collection_api.get_collection(
            collection_id=collection_id,
            account_id=account_id or self.account_id,
        )

        return Collection.model_validate(collection.model_dump())

    def _validate_create_collection_parameters(
        self,
        llm_provider: str,
        url: Optional[str] = None,
        llm: Optional[str] = None,
    ) -> None:
        if llm_provider == LLMProvider.HuggingFace.value and not url:
            raise ValueError(
                f"URL parameter is required if {llm_provider} is used as LLM provider."
            )
        elif llm_provider == LLMProvider.OpenAI.value and not llm:
            raise ValueError(
                f"LLM parameter is required if {llm_provider} is used as LLM provider."
            )

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
        Creates a new collection with the specified parameters.

        This method creates a new collection based on the provided collection object.

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

        Example
        -------
        User-Provided:
        >>> vantage_client = VantageClient(...)
        >>> upe_collection = UserProvidedEmbeddingsCollection(
                collection_id="upe-test-collection",
                embeddings_dimension=3,
            )
        >>> new_collection = vantage_client.create_collection(
                collection=upe_collection,
            )
        >>> print(new_collection.id)
        "upe-test-collection"

        Vantage-Managed:
        >>> vantage_client = VantageClient(...)
        >>> openai_collection = OpenAICollection(
            collection_id="openai-test-collection",
            external_account_id="123_id",
            llm="text-embedding-ada-002",
            embeddings_dimension=1536,
        )
        >>> new_collection = vantage_client.create_collection(
                collection=upe_collection,
            )
        >>> print(new_collection.id)
        "openai-test-collection"
        """

        if hasattr(collection, "secondary_external_accounts"):
            collection._convert_secondary_external_accounts(
                collection.secondary_external_accounts
            )

        create_collection_request = CreateCollectionRequest(
            collection_id=collection.collection_id,
            collection_name=collection.collection_name,
            user_provided_embeddings=bool(collection.user_provided_embeddings),
            embeddings_dimension=int(collection.embeddings_dimension),
            external_key_id=getattr(collection, 'external_account_id', None),
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
        Updates an existing collection's details such as its name, associated external key ID, and secondary accounts.
        It checks for the existence of the collection within the specified account and raises an exception if the
        collection does not exist. Upon successful update, it returns an updated Collection object.

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

        Example
        -------
        >>> vantage_client = VantageClient(...)
        >>> updated_collection = vantage_client.update_collection(
                collection_id="my-collection",
                collection_name="Updated Collection Name",
            )
        >>> print(updated_collection.name)
        "Updated Collection Name"
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
                    f"Only collections which are using {LLMProvider.OpenAI.value} as LLM provider can have secondary external accounts."
                )

            secondary_external_accounts = [
                CollectionModifiableSecondaryExternalAccountsInner(
                    actual_instance=OpenAPISecondaryExternalAccount(
                        external_account_id=account.external_account_id,
                        external_type=account.external_type,
                    )
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
        Deletes a specific collection identified by its collection ID within a specified account. It first verifies
        the existence of the collection in the account and raises an exception if the collection does not exist. Upon
        successful deletion, it returns the Collection object that was deleted.

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

        Example
        -------
        >>> vantage_client = VantageClient(...)
        >>> vantage_client.delete_collection(collection_id="my-collection")
        """

        self.management_api.collection_api.delete_collection(
            collection_id=collection_id,
            account_id=account_id if account_id else self.account_id,
        )

    # endregion

    # region Search

    def _prepare_search_query(
        self,
        collection_id: str,
        accuracy: float = 0.3,
        page: Optional[int] = None,
        page_count: Optional[int] = None,
        boolean_filter: Optional[str] = None,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
        sort_mode: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> GlobalSearchProperties:
        collection = GlobalSearchPropertiesCollection(
            collection_id=collection_id,
            accuracy=accuracy,
            account_id=account_id or self.account_id,
        )

        search_filter = (
            GlobalSearchPropertiesFilter(
                boolean_filter=boolean_filter,
            )
            if boolean_filter
            else None
        )

        pagination = (
            GlobalSearchPropertiesPagination(
                page=page,
                count=page_count,
            )
            if page
            else None
        )

        sort = (
            GlobalSearchPropertiesSort(
                field=sort_field,
                order=sort_order,
                mode=sort_mode,
            )
            if sort_field
            else None
        )

        return GlobalSearchProperties(
            collection=collection,
            filter=search_filter,
            pagination=pagination,
            sort=sort,
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

    def semantic_search(
        self,
        text: str,
        collection_id: str,
        accuracy: float = 0.3,
        page: Optional[int] = None,
        page_count: Optional[int] = None,
        boolean_filter: Optional[str] = None,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
        sort_mode: Optional[str] = None,
        vantage_api_key: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> SearchResult:
        """
        Performs a search within a specified collection using a text query,
        with optional parameters for accuracy, pagination, and a boolean filter for refined
        search criteria.

        Parameters
        ----------
        text : str
            The text query for the semantic search.
        collection_id : str
            The ID of the collection to search within.
        accuracy : float, optional
            The accuracy threshold for the search.
            Defaults to 0.3.
        page : Optional[int], optional
            The page number for pagination.
            Defaults to None.
        page_count : Optional[int], optional
            The number of results per page for pagination.
            Defaults to None.
        boolean_filter : Optional[str], optional
            A boolean filter string for refining search results.
            Defaults to None.
        sort_field: Optional[str], optional
            Meta field name for sorting search results on.
            If set, other sort_ fields will be taken into account.
            Defaults to None.
        sort_order: Optional[str], optional
            Sort order. Possible values [asc, desc].
            Defaults to desc.
        sort_mode: Optional[str], optional
            Sort mode. Possible values [semantic_threshold, field_selection].
            Defaults to field_selection.
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
        """

        vantage_api_key = self._vantage_api_key_check(vantage_api_key)

        search_properties = self._prepare_search_query(
            collection_id,
            accuracy,
            page,
            page_count,
            boolean_filter,
            sort_field,
            sort_order,
            sort_mode,
            account_id,
        )

        query = SemanticSearchQuery(
            text=text,
            collection=search_properties.collection,
            filter=search_properties.filter,
            pagination=search_properties.pagination,
            sort=search_properties.sort,
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
        embedding: List[int],
        collection_id: str,
        accuracy: float = 0.3,
        page: Optional[int] = None,
        page_count: Optional[int] = None,
        boolean_filter: Optional[str] = None,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
        sort_mode: Optional[str] = None,
        vantage_api_key: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> SearchResult:
        """
        Performs a search within a specified collection using an embedding vector,
        with optional parameters for accuracy, pagination, and a boolean filter for refined
        search criteria.

        Parameters
        ----------
        embedding : List[int]
            The embedding vector used for the search.
        collection_id : str
            The ID of the collection to search within.
        accuracy : float, optional
            The accuracy threshold for the search.
            Defaults to 0.3.
        page : Optional[int], optional
            The page number for pagination.
            Defaults to None.
        page_count : Optional[int], optional
            The number of results per page for pagination.
            Defaults to None.
        boolean_filter : Optional[str], optional
            A boolean filter string for refining search results.
            Defaults to None.
        sort_field: Optional[str], optional
            Meta field name for sorting search results on.
            If set, other sort_ fields will be taken into account.
            Defaults to None.
        sort_order: Optional[str], optional
            Sort order. Possible values [asc, desc].
            Defaults to desc.
        sort_mode: Optional[str], optional
            Sort mode. Possible values [semantic_threshold, field_selection].
            Defaults to field_selection.
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
        """

        vantage_api_key = self._vantage_api_key_check(vantage_api_key)

        search_properties = self._prepare_search_query(
            collection_id,
            accuracy,
            page,
            page_count,
            boolean_filter,
            sort_field,
            sort_order,
            sort_mode,
            account_id,
        )

        query = EmbeddingSearchQuery(
            embedding=embedding,
            collection=search_properties.collection,
            filter=search_properties.filter,
            pagination=search_properties.pagination,
            sort=search_properties.sort,
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
        accuracy: float = 0.3,
        page: Optional[int] = None,
        page_count: Optional[int] = None,
        boolean_filter: Optional[str] = None,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
        sort_mode: Optional[str] = None,
        account_id: Optional[str] = None,
        vantage_api_key: Optional[str] = None,
    ) -> SearchResult:
        """
        Performs a "More Like This" search to find documents similar to a specified
        document within a specified collection using optional parameters for
        accuracy, pagination, and a boolean filter for refined search criteria.

        Parameters
        ----------
        document_id : str
            The ID of the document to find similar documents to.
        collection_id : str
            The ID of the collection to search within.
        accuracy : float, optional
            The accuracy threshold for the search.
            Defaults to 0.3.
        page : Optional[int], optional
            The page number for pagination.
            Defaults to None.
        page_count : Optional[int], optional
            The number of results per page for pagination.
            Defaults to None.
        boolean_filter : Optional[str], optional
            A boolean filter string for refining search results.
            Defaults to None.
        sort_field: Optional[str], optional
            Meta field name for sorting search results on.
            If set, other sort_ fields will be taken into account.
            Defaults to None.
        sort_order: Optional[str], optional
            Sort order. Possible values [asc, desc].
            Defaults to desc.
        sort_mode: Optional[str], optional
            Sort mode. Possible values [semantic_threshold, field_selection].
            Defaults to field_selection.
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
        """

        vantage_api_key = self._vantage_api_key_check(vantage_api_key)

        search_properties = self._prepare_search_query(
            collection_id,
            accuracy,
            page,
            page_count,
            boolean_filter,
            sort_field,
            sort_order,
            sort_mode,
            account_id,
        )

        query = MoreLikeThisQuery(
            document_id=document_id,
            collection=search_properties.collection,
            filter=search_properties.filter,
            pagination=search_properties.pagination,
            sort=search_properties.sort,
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
        accuracy: float = 0.3,
        page: Optional[int] = None,
        page_count: Optional[int] = None,
        boolean_filter: Optional[str] = None,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
        sort_mode: Optional[str] = None,
        account_id: Optional[str] = None,
        vantage_api_key: Optional[str] = None,
    ) -> SearchResult:
        """
        Performs a "More Like These" search to find documents similar to a specified list
        of MoreLikeTheseItem objects within a specified collection using optional parameters for
        accuracy, pagination, and a boolean filter for refined search criteria.

        Parameters
        ----------
        more_like_these : list[MoreLikeTheseItem]
            The list of "MoreLikeTheseItem" objects to find similar documents to.
        collection_id : str
            The ID of the collection to search within.
        accuracy : float, optional
            The accuracy threshold for the search.
            Defaults to 0.3.
        page : Optional[int], optional
            The page number for pagination.
            Defaults to None.
        page_count : Optional[int], optional
            The number of results per page for pagination.
            Defaults to None.
        boolean_filter : Optional[str], optional
            A boolean filter string for refining search results.
            Defaults to None.
        sort_field: Optional[str], optional
            Meta field name for sorting search results on.
            If set, other sort_ fields will be taken into account.
            Defaults to None.
        sort_order: Optional[str], optional
            Sort order. Possible values [asc, desc].
            Defaults to desc.
        sort_mode: Optional[str], optional
            Sort mode. Possible values [semantic_threshold, field_selection].
            Defaults to field_selection.
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
        """

        vantage_api_key = self._vantage_api_key_check(vantage_api_key)

        search_properties = self._prepare_search_query(
            collection_id,
            accuracy,
            page,
            page_count,
            boolean_filter,
            sort_field,
            sort_order,
            sort_mode,
            account_id,
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
        )

        result = self.search_api.api.more_like_these_search(
            collection_id=collection_id,
            account_id=account_id or self.account_id,
            more_like_these_query=query,
            _headers={"authorization": f"Bearer {vantage_api_key}"},
        )

        return SearchResult.model_validate(result.model_dump())

    # endregion

    # region Upload - Documents

    def upload_documents_from_jsonl(
        self,
        collection_id: str,
        documents: str,
        batch_identifier: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> None:
        """
        Uploads documents to a specified collection from a string containing JSONL-formatted documents.
        The `documents` string is expected to be in JSONL format, where each line is a valid JSON
        document.

        Parameters
        ----------
        collection_id : str
            The unique identifier of the collection to which the documents will be uploaded.
        documents : str
            A string containing the documents to be uploaded, formatted as JSONL.
        batch_identifier : Optional[str], optional
            An optional identifier provided by the user to track the batch of document uploads.
        account_id : Optional[str], optional
            The account ID to which the collection belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Example
        -------
        >>> vantage_client = VantageClient(...)
        >>> documents_jsonl = '{"id": "1", "text": "Example text", "meta_color": "green", "meta_something": "value", "embeddings": [1,2,3, ...]}\\n{"id": "2", "text": "Lorem ipsum", "meta_color": "blue", "meta_something": "value", "embeddings": [4,5,6, ...]}' # noqa: E501
        >>> vantage_client.upload_documents_from_jsonl(
                collection_id="my-collection",
                documents=documents_jsonl,
            )
        # This will upload two documents to "my-collection".

        Note
        -------
        Documents in the JSONL file should be in the right format:

        Uploading to user-provided collection (`embeddings` field is included):
        {"id": "1", "text": "Example text", "meta_color": "green", "meta_something": "value", "embeddings": [1,2,3, ...]}


        Uploading to vantage-managed collection (`embeddings` field is excluded):
        {"id": "1", "text": "Example text", "meta_color": "green", "meta_something": "value"}

        Metadata fields should all have `meta_` prefix.
        """

        self.management_api.documents_api.upload_documents(
            body=documents,
            account_id=account_id if account_id else self.account_id,
            collection_id=collection_id,
            customer_batch_identifier=batch_identifier,
        )

    def upload_documents_from_path(
        self,
        collection_id: str,
        file_path: str,
        batch_identifier: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> None:
        """
        Uploads documents to a specified collection from a JSONL file located at a given file path.
        This method checks if the file exists at the specified path and raises a FileNotFoundError if it does not.
        It then reads the file and uploads the documents contained within the file to the specified
        collection using the `upload_documents_from_jsonl` method.

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

        Example
        -------
        >>> vantage_client = VantageClient()
        >>> vantage_client.upload_documents_from_path(
                collection_id="my-collection",
                file_path="/path/to/documents.jsonl",
            )
        # This will upload documents from "/path/to/documents.jsonl" to "my-collection".

        Note
        -------
        Documents in the JSONL file should be in the right format:

        Uploading to user-provided collection (`embeddings` field is included):
        {"id": "1", "text": "Example text", "meta_color": "green", "meta_something": "value", "embeddings": [1,2,3, ...]} # noqa: E501


        Uploading to vantage-managed collection (`embeddings` field is excluded):
        {"id": "1", "text": "Example text", "meta_color": "green", "meta_something": "value"}

        Metadata fields should all have `meta_` prefix.
        """

        if not exists(file_path):
            raise FileNotFoundError(f"File \"{file_path}\" not found.")

        file = open(file_path, "rb")
        file_content = file.read().decode(self._default_encoding)
        self.upload_documents_from_jsonl(
            collection_id=collection_id,
            documents=file_content,
            batch_identifier=batch_identifier,
            account_id=account_id,
        )

    # endregion

    # region Upload - Embeddings

    def _upload_embedding(self, upload_url: str, upload_content) -> int:
        response = requests.put(
            upload_url,
            data=upload_content,
        )

        if response.status_code != 200:
            raise VantageFileUploadError(response.reason, response.status_code)

        return response.status_code

    def upload_embeddings_from_bytes(
        self,
        collection_id: str,
        content: bytes,
        file_size: int,
        batch_identifier: Optional[str],
        account_id: Optional[str] = None,
    ) -> int:
        """
        Uploads embeddings in parquet format to a collection.

        Parameters
        ----------
        collection_id : str
            The unique identifier of the collection embeddings are being uploaded.
        account_id : Optional[str], optional
            The account ID to which the collection belongs.
            If not provided, the instance's account ID is used.
            Defaults to None
        content: bytes
            Embeddings content as bytes.
        file_size: int
            Size of contents being uploaded, in bytes.
        parquet_file_name: str
        batch_identifier : Optional[str], optional
            An optional identifier provided by the user to track the batch of document uploads.
            Identifier needs to end with '.parquet',if it doesn't, it will be
            automatically added.
            If none is provided, it will be generated automatically.

        Returns
        -------
        int
            HTTP status of upload execution.

        Example
        -------
        >>> vantage_client = VantageClient(...)
        >>> vantage_client.upload_parquet_embedding(
            collection_id="my-collection",
            content=parquet_content_as_bytes,
            file_size=1000,
            batch_identifier="my-embeddings.parquet"
        )
        """

        if batch_identifier is None:
            batch_identifier = f"{uuid.uuid4}.parquet"
        elif not batch_identifier.endswith(".parquet"):
            batch_identifier = f"{batch_identifier}.parquet"

        browser_upload_url = self._get_browser_upload_url(
            collection_id=collection_id,
            file_size=file_size,
            parquet_file_name=batch_identifier,
            account_id=account_id,
        )

        return self._upload_embedding(
            upload_url=browser_upload_url.upload_url,
            upload_content=content,
        )

    def upload_embeddings_from_parquet(
        self,
        collection_id: str,
        file_path: str,
        account_id: Optional[str] = None,
    ) -> int:
        """
        Uploads embeddings from a parquet file to a collection.

        Parameters
        ----------
        collection_id : str
            The unique identifier of the collection
            embeddings are being uploaded to.
        file_path : str, optional
            Path to the parquet file in a filesystem.
        account_id : Optional[str], optional
            The account ID to which the collection belongs.
            If not provided, the instance's account ID is used.
            Defaults to None

        Returns
        -------
        int
            HTTP status of upload execution.

        Example
        -------
        >>> vantage_client = VantageClient(...)
        >>> vantage_client.upload_parquet_embedding(
            collection_id="my-collection",
            content=parquet_content_as_bytes,
            file_size=1000,
            batch_identifier="my-embeddings.parquet"
        )
        """

        if not exists(file_path):
            raise FileNotFoundError(f"File \"{file_path}\" not found.")
        file_name = ntpath.basename(file_path)

        if not file_path.endswith(".parquet"):
            raise ValueError("File mast be a parquet file.")

        file_size = Path(file_path).stat().st_size
        file = open(file_path, "rb")
        file_content = file.read()
        return self.upload_embeddings_from_bytes(
            collection_id=collection_id,
            content=file_content,
            file_size=file_size,
            batch_identifier=file_name,
            account_id=account_id,
        )

    # endregion

    def _document_to_collection_compatibility_check(
        self,
        collection: Collection,
        document: Union[
            UserProvidedEmbeddingsDocument, VantageManagedEmbeddingsDocument
        ],
    ) -> None:
        if collection.user_provided_embeddings and isinstance(
            document, VantageManagedEmbeddingsDocument
        ):
            raise ValueError(
                f"Embeddings are required for User-provided embeddings collection. Please provide a list of {UserProvidedEmbeddingsDocument.__name__} objects."
            )
        elif not collection.user_provided_embeddings and isinstance(
            document, UserProvidedEmbeddingsDocument
        ):
            raise ValueError(
                f"Embeddings are not required for Vantage-managed embeddings collection. Please provide a list of {VantageManagedEmbeddingsDocument.__name__} objects."
            )

    def upsert(
        self,
        collection_id: str,
        documents: Union[
            List[VantageManagedEmbeddingsDocument],
            List[UserProvidedEmbeddingsDocument],
        ],
        account_id: Optional[str] = None,
    ):
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

        self.upload_documents_from_jsonl(
            collection_id=collection_id,
            documents=vantage_documents_jsonl,
            account_id=account_id or self.account_id,
        )
