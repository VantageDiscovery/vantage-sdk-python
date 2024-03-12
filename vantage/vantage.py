from __future__ import annotations

import ntpath
import uuid
from os.path import exists
from pathlib import Path
from typing import List, Optional

from vantage.config import (
    API_HOST_VERSION,
    AUTH_ENDPOINT,
    DEFAULT_API_HOST,
    DEFAULT_AUTH_HOST,
    DEFAULT_ENCODING,
)
from vantage.core.base import AuthorizationClient, AuthorizedApiClient
from vantage.core.http.models import (
    AccountModifiable,
    CollectionModifiable,
    CreateCollectionRequest,
    EmbeddingSearchQuery,
    ExternalAPIKeyModifiable,
    GlobalSearchPropertiesCollection,
    GlobalSearchPropertiesFilter,
    GlobalSearchPropertiesPagination,
    MLTheseTheseInner,
    MoreLikeTheseQuery,
    MoreLikeThisQuery,
    SemanticSearchQuery,
)
from vantage.core.management import ManagementAPI
from vantage.core.search import SearchAPI
from vantage.exceptions import VantageValueError
from vantage.model.account import Account
from vantage.model.collection import Collection, CollectionUploadURL
from vantage.model.keys import ExternalAPIKey, VantageAPIKey
from vantage.model.search import (
    GlobalSearchProperties,
    MoreLikeTheseItem,
    SearchResult,
)


class VantageClient:
    def __init__(
        self,
        management_api: ManagementAPI,
        search_api: SearchAPI,
        account_id: str,
        vantage_api_key: Optional[str] = None,
        host: Optional[str] = None,
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

        management_api = ManagementAPI.from_defaults(api_client)
        search_api = SearchAPI(api_client)

        return cls(
            management_api,
            search_api,
            account_id,
            vantage_api_key,
            host,
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

        management_api = ManagementAPI.from_defaults(api_client)
        search_api = SearchAPI(api_client)

        return cls(
            management_api,
            search_api,
            account_id,
            vantage_api_key,
            host,
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

        result = self.management_api.account_api.api.get_account(
            account_id=account_id if account_id else self.account_id
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

        result = self.management_api.account_api.api.update_account(
            account_id=account_id if account_id else self.account_id,
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

        keys = (
            self.management_api.vantage_api_keys_api.api.get_vantage_api_keys(
                account_id=account_id if account_id else self.account_id,
            )
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

        key = self.management_api.vantage_api_keys_api.api.get_vantage_api_key(
            account_id=account_id if account_id else self.account_id,
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

        keys = self.management_api.external_api_keys_api.api.get_external_api_keys(
            account_id=account_id if account_id else self.account_id,
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

        key = (
            self.management_api.external_api_keys_api.api.get_external_api_key(
                account_id=account_id if account_id else self.account_id,
                external_key_id=external_key_id,
            )
        )

        return ExternalAPIKey.model_validate(key.model_dump())

    def create_external_api_key(
        self,
        llm_provider: str,
        llm_secret: str,
        url: Optional[str] = None,
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
            The provider of the Large Language Model (LLM) service.
            Supported options are: OpenAI and HuggingFace (Hugging)
        llm_secret : str
            The secret key for accessing the LLM service.
        url : Optional[str], optional
            Currently not in use
            Defaults to None.
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
            url=url, llm_provider=llm_provider, llm_secret=llm_secret
        )

        key = self.management_api.external_api_keys_api.api.create_external_api_key(
            account_id=account_id if account_id else self.account_id,
            external_api_key_modifiable=external_api_key_modifiable,
        )

        return ExternalAPIKey.model_validate(key.model_dump())

    def update_external_api_key(
        self,
        external_key_id: str,
        llm_provider: str,
        llm_secret: str,
        url: Optional[str] = None,
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
            The new provider of the Large Language Model (LLM) service.
        llm_secret : str
            The new secret key for accessing the LLM service.
        url : Optional[str], optional
            The new URL associated with the external API key, indicating the endpoint of the external service.
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
            url=url, llm_provider=llm_provider, llm_secret=llm_secret
        )

        key = self.management_api.external_api_keys_api.api.update_external_api_key(
            account_id=account_id if account_id else self.account_id,
            external_key_id=external_key_id,
            external_api_key_modifiable=external_api_key_modifiable,
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

        self.management_api.external_api_keys_api.api.delete_external_api_key(
            account_id=account_id if account_id else self.account_id,
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
            account_id=account_id if account_id else self.account_id
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

        url = self.management_api.collection_api.api.get_browser_upload_url(
            collection_id=collection_id,
            file_size=file_size,
            customer_batch_identifier=parquet_file_name,
            account_id=account_id if account_id else self.account_id,
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

        collections = self.management_api.collection_api.api.list_collections(
            account_id=account_id if account_id else self.account_id
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

        collection = self.management_api.collection_api.api.get_collection(
            collection_id=collection_id,
            account_id=account_id if account_id else self.account_id,
        )

        return Collection.model_validate(collection.model_dump())

    def create_collection(
        self,
        collection_id: str,
        embeddings_dimension: int,
        collection_name: Optional[str] = None,
        user_provided_embeddings: Optional[bool] = False,
        llm: Optional[str] = None,
        external_key_id: Optional[str] = None,
        collection_preview_url_pattern: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> Collection:
        """
        Creates a new collection with the specified parameters.

        This method creates a new collection identified by a unique collection ID.
        It checks for the uniqueness of the collection ID within the specified account
        and raises an exception if a collection with the given ID already exists.
        The collection can optionally be configured to use user-provided embeddings
        or leverage a Large Language Model (LLM) for embeddings generation.
        Additional parameters allow specifying an external key for API integration,
        a preview URL pattern for collection items, and the dimensionality of embeddings.

        Parameters
        ----------
        collection_id : str
            The unique identifier for the new collection.
            It can only contain lowercase letters [a-z], digits [0-9] and a hypen [-].
            The maximum length for a colleciton ID is 36 characters.
            It can not be changed after the collection is created.
        collection_name : str
            The name of the new collection.
        embeddings_dimension : int
            The dimensionality of the embeddings for the collection items.
        user_provided_embeddings : Optional[bool], optional
            Indicates whether embeddings are provided by the user (True)
            or managed by Vantage (False). Defaults to False.
        llm : Optional[str], optional
            The identifier of the Large Language Model used for generating embeddings, if applicable.
        external_key_id : Optional[str], optional
            The external key ID used for API integration, if applicable.
        collection_preview_url_pattern : Optional[str], optional
            A URL pattern for previewing items in the collection, if applicable.
        account_id : Optional[str], optional
            The account ID to which the collection belongs.
            If not provided, the instance's account ID is used.
            Defaults to None.

        Returns
        -------
        Collection
            A Collection object representing the newly created collection.

        Example
        -------
        User-Provided:
        >>> vantage_client = VantageClient(...)
        >>> new_collection = vantage_client.create_collection(
                collection_id="user-provided",
                collection_name="My Collection",
                embeddings_dimension=1536,
                user_provided_embeddings=True,
                llm="text-embedding-ada-002",
                external_key_id="external_key_123",
            )
        >>> print(new_collection.id)
        "user-provided"

        Vantage-Managed:
        >>> vantage_client = VantageClient(...)
        >>> new_collection = vantage_client.create_collection(
                collection_id="vantage-managed",
                collection_name="My Collection",
                embeddings_dimension=1536,
                user_provided_embeddings=False,
            )
        >>> print(new_collection.id)
        "vantage-managed"
        """

        collection_name = (
            collection_name
            if collection_name
            else f"Collection [{collection_id}]"
        )

        create_collection_request = CreateCollectionRequest(
            external_key_id=(
                external_key_id if not user_provided_embeddings else None
            ),
            collection_id=collection_id,
            collection_name=collection_name,
            embeddings_dimension=int(embeddings_dimension),
            user_provided_embeddings=bool(user_provided_embeddings),
            llm=llm if not user_provided_embeddings else None,
            collection_preview_url_pattern=collection_preview_url_pattern,
        )

        collection = self.management_api.collection_api.api.create_collection(
            create_collection_request=create_collection_request,
            account_id=account_id if account_id else self.account_id,
        )

        return Collection.model_validate(collection.model_dump())

    def update_collection(
        self,
        collection_id: str,
        collection_name: Optional[str] = None,
        external_key_id: Optional[str] = None,
        collection_preview_url_pattern: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> Collection:
        """
        Updates an existing collection's details such as its name, associated external key ID, and preview URL pattern.
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
        collection_preview_url_pattern : Optional[str], optional
            New URL pattern for previewing items in the collection, if updating.
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

        collection_modifiable = CollectionModifiable(
            external_key_id=external_key_id,
            collection_preview_url_pattern=collection_preview_url_pattern,
            collection_name=collection_name,
        )

        collection = self.management_api.collection_api.api.update_collection(
            collection_id=collection_id,
            collection_modifiable=collection_modifiable,
            account_id=account_id if account_id else self.account_id,
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

        self.management_api.collection_api.api.delete_collection(
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
        account_id: Optional[str] = None,
    ) -> GlobalSearchProperties:
        collection = GlobalSearchPropertiesCollection(
            collection_id=collection_id,
            accuracy=accuracy,
            account_id=account_id if account_id else self.account_id,
        )

        if boolean_filter:
            search_filter = GlobalSearchPropertiesFilter(
                boolean_filter=boolean_filter,
            )
        else:
            search_filter = None

        if page:
            pagination = GlobalSearchPropertiesPagination(
                page=page,
                count=page_count,
            )
        else:
            pagination = None

        return GlobalSearchProperties(
            collection=collection,
            filter=search_filter,
            pagination=pagination,
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
            account_id,
        )

        query = SemanticSearchQuery(
            text=text,
            collection=search_properties.collection,
            filter=search_properties.filter,
            pagination=search_properties.pagination,
        )

        result = self.search_api.api.semantic_search(
            query,
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
            account_id,
        )

        query = EmbeddingSearchQuery(
            embedding=embedding,
            collection=search_properties.collection,
            filter=search_properties.filter,
            pagination=search_properties.pagination,
        )

        result = self.search_api.api.embedding_search(
            query,
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
            account_id,
        )

        query = MoreLikeThisQuery(
            document_id=document_id,
            collection=search_properties.collection,
            filter=search_properties.filter,
            pagination=search_properties.pagination,
        )

        result = self.search_api.api.more_like_this_search(
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
        )

        result = self.search_api.api.more_like_these_search(
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

        self.management_api.documents_api.api.upload_documents(
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

        return self.management_api.collection_api.upload_embedding(
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
            parquet_file_name=file_name,
            account_id=account_id,
        )

    # endregion
