from __future__ import annotations

from os.path import exists
from pathlib import Path
from typing import List, Optional

from pydantic_core._pydantic_core import ValidationError

from vantage.core.base import AuthorizationClient, AuthorizedApiClient
from vantage.core.http.exceptions import (
    ApiAttributeError,
    ApiException,
    ApiKeyError,
    ApiValueError,
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    OpenApiException,
    ServiceException,
    UnauthorizedException,
)
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
from vantage.exceptions import (
    VantageForbiddenError,
    VantageInvalidRequestError,
    VantageInvalidResponseError,
    VantageNotFoundError,
    VantageServiceError,
    VantageUnauthorizedError,
    VantageValueError,
)
from vantage.model.account import Account
from vantage.model.collection import Collection, CollectionUploadURL
from vantage.model.keys import ExternalAPIKey, VantageAPIKey
from vantage.model.search import MoreLikeThese, SearchResult


def _parse_exception(exception: Exception, response=None) -> Exception:
    if isinstance(exception, BadRequestException):
        return VantageInvalidRequestError(
            reason=exception.reason,
            status=exception.status,
            response=exception.body,
        )

    if isinstance(exception, NotFoundException):
        return VantageNotFoundError(message=exception.reason)

    if isinstance(exception, UnauthorizedException):
        return VantageUnauthorizedError("")

    if isinstance(exception, ForbiddenException):
        return VantageForbiddenError("")

    if isinstance(exception, ServiceException):
        return VantageServiceError(
            reason=exception.reason,
            status=exception.status,
            response=exception.body,
        )

    if isinstance(exception, ApiValueError):
        return VantageInvalidRequestError(
            reason=exception.reason,
            status=exception.status,
            response=exception.body,
        )

    if isinstance(exception, ApiAttributeError):
        return VantageInvalidRequestError(
            reason=exception.reason,
            status=exception.status,
            response=exception.body,
        )

    if isinstance(exception, ApiKeyError):
        return VantageInvalidRequestError(
            reason=exception.reason,
            status=exception.status,
            response=exception.body,
        )

    if isinstance(exception, ApiException):
        return VantageServiceError(
            reason=exception.reason,
            status=exception.status,
            response=exception.body,
        )

    if isinstance(exception, OpenApiException):
        return VantageServiceError(
            reason=exception.reason,
            status=exception.status,
            response=exception.body,
        )

    if isinstance(exception, ValidationError):
        return VantageInvalidResponseError(
            error_message=exception.title, validation_error=exception
        )

    return exception


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
        The `VantageClient` class is the main entry point for interacting with Vantage Discovery via the Python SDK.
        It is used to create, delete, and manage your accounts, collections and keys.
        """
        self.management_api = management_api
        self.search_api = search_api
        self.account_id = account_id
        self.vantage_api_key = vantage_api_key
        self.host = host
        self._default_encoding = "utf-8"

    @classmethod
    def using_jwt_token(
        cls,
        vantage_api_jwt_token: str,
        account_id: str,
        vantage_api_key: Optional[str] = None,
        api_host: Optional[str] = "https://api.vanta.ge",
    ) -> VantageClient:
        """
        Initializes the VantageClient using JWT token.

        Parameters
        ----------
            vantage_api_jwt_token: str
                The JWT token to use for authentication.
            account_id: str
                Account ID TODO
            vantage_api_key: str
                Vantage API Key TODO
            api_host: str
                API host, if not provided default host will be used.

        Returns
        -------
            VantageClient
                Vantage client initialized using JWT token.
        """
        host = f"{api_host}/v1"
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
        api_host: Optional[str] = "https://api.vanta.ge",
        auth_host: Optional[str] = "https://auth.vanta.ge",
    ) -> VantageClient:
        """
        Initializes the VantageClient using client credentials.

        Parameters
        ----------
            vantage_client_id: str
                Vantage Client ID TODO
            vantage_client_secret: str
                Vantage Client Secret TODO
            account_id: str
                Account ID TODO
            vantage_api_key: str
                Vantage API Key TODO
            api_host: str
                Vantage API host, if not provided default API host will be used.
            auth_host: str
                Vantage auth host, if not provided default auth host will be used.

        Returns
        -------
            VantageClient
                Vantage client initialized using client credentials.
        """
        host = f"{api_host}/v1"
        auth_endpoint = f"{auth_host}/oauth/token"
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
            If None, the account ID of the current instance is used.

        Returns
        -------
        Account
            An Account object containing the details of the requested account.

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> account = vantage_client.get_account()
        >>> print(account.account_name)
        "Example Account Name"
        """

        try:
            result = self.management_api.account_api.api.get_account(
                account_id=account_id if account_id else self.account_id
            )
            return Account.model_validate(result.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

    # TODO: Check what fields are mandatory
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
            If None, the account ID of the current instance is used.

        Returns
        -------
        Account
            An updated Account object reflecting the changes made.

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> updated_account = vantage_client.update_account(account_name="New Account Name")
        >>> print(updated_account.account_name)
        "New Account Name"
        """

        account_modifiable = AccountModifiable(account_name=account_name)

        try:
            result = self.management_api.account_api.api.update_account(
                account_id=account_id if account_id else self.account_id,
                account_modifiable=account_modifiable,
            )
            return Account.model_validate(result.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

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
            If None, the account ID of the current instance is used.

        Returns
        -------
        List[VantageAPIKey]
            A list of VantageAPIKey objects, each representing a Vantage API key associated with the account.

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> vantage_api_keys = vantage_client.get_vantage_api_keys()
        >>> for key in vantage_api_keys:
        ...     print(key.vantage_api_key_value)
        "12345"
        "54321"
        """

        try:
            keys = self.management_api.vantage_api_keys_api.api.get_vantage_api_keys(
                account_id=account_id if account_id else self.account_id,
            )

            return [
                VantageAPIKey.model_validate(key.actual_instance.model_dump())
                for key in keys
            ]
        except Exception as exception:
            raise _parse_exception(exception)

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
            If None, the account ID of the current instance is used.

        Returns
        -------
        VantageAPIKey
            A VantageAPIKey object containing the details of the requested API key.

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> vantage_api_key = vantage_client.get_vantage_api_key(vantage_api_key_id="api_key_12345")
        >>> print(vantage_api_key.vantage_api_key_value)
        "12345"
        """

        try:
            key = self.management_api.vantage_api_keys_api.api.get_vantage_api_key(
                account_id=account_id if account_id else self.account_id,
                vantage_api_key_id=vantage_api_key_id,
            )
            return VantageAPIKey.model_validate(key.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

    # endregion

    # region External API keys

    def create_external_api_key(
        self,
        url: str,
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
        url : str
            TODO: ?
        llm_provider : str
            The provider of the Large Language Model (LLM) service.
            Supported options are: OpenAI and HuggingFace (Hugging)
        llm_secret : str
            The secret key for accessing the LLM service.
        account_id : Optional[str], optional
            The unique identifier of the account for which the external API key is to be created.
            If None, the account ID of the current instance is used.

        Returns
        -------
        ExternalAPIKey
            An ExternalAPIKey object containing the details of the newly created API key.

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> external_api_key = vantage_client.create_external_api_key(
        ...     url="https://example.com/api",
        ...     llm_provider="OpenAI",
        ...     llm_secret="secret123",
        ... )
        >>> print(external_api_key.external_key_id)
        "external_key_123"
        """

        external_api_key_modifiable = ExternalAPIKeyModifiable(
            url=url, llm_provider=llm_provider, llm_secret=llm_secret
        )

        try:
            key = self.management_api.external_api_keys_api.api.create_external_api_key(
                account_id=account_id if account_id else self.account_id,
                external_api_key_modifiable=external_api_key_modifiable,
            )

            return ExternalAPIKey.model_validate(key.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

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
            If None, the account ID of the current instance is used.

        Returns
        -------
        List[ExternalAPIKey]
            A list of ExternalAPIKey objects, each representing an external API key associated with the account.

        Examples
        --------
        >>> vantage_client = VantageClient()
        >>> external_api_keys = vantage_client.get_external_api_keys()
        >>> for key in external_api_keys:
        ...     print(key.external_key_id)
        "external_key_123"
        "external_key_321"
        """

        try:
            keys = self.management_api.external_api_keys_api.api.get_external_api_keys(
                account_id=account_id if account_id else self.account_id,
            )
            return [
                ExternalAPIKey.model_validate(key.actual_instance.model_dump())
                for key in keys
            ]
        except Exception as exception:
            raise _parse_exception(exception)

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
            If None, the account ID of the current instance is used.

        Returns
        -------
        ExternalAPIKey
            An ExternalAPIKey object containing the details of the requested external API key.

        Examples
        --------
        >>> vantage_client = VantageClient()
        >>> external_api_key = vantage_client.get_external_api_key(external_key_id="external_key_123")
        >>> print(external_api_key.llm_provider)
        "OpenAI"
        """

        try:
            key = self.management_api.external_api_keys_api.api.get_external_api_key(
                account_id=account_id if account_id else self.account_id,
                external_key_id=external_key_id,
            )

            return ExternalAPIKey.model_validate(key.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

    def update_external_api_key(
        self,
        external_key_id: str,
        url: str,
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
        url : str
            The new URL associated with the external API key, indicating the endpoint of the external service.
        llm_provider : str
            The new provider of the Large Language Model (LLM) service.
        llm_secret : str
            The new secret key for accessing the LLM service.
        account_id : Optional[str], optional
            The unique identifier of the account to which the external API key is associated.
            If None, the account ID of the current instance is used.

        Returns
        -------
        ExternalAPIKey
            An ExternalAPIKey object containing the updated details of the external API key.

        Examples
        --------
        >>> vantage_client = VantageClient()
        >>> updated_external_api_key = vantage_client.update_external_api_key(
        ...     external_key_id="external_key_123",
        ...     url="https://newexample.com/api",
        ...     llm_provider="OpenAI",
        ...     llm_secret="new_secret_123",
        ...     account_id="12345"
        ... )
        >>> print(updated_external_api_key.llm_secret)
        "new_secret_123"
        """

        external_api_key_modifiable = ExternalAPIKeyModifiable(
            url=url, llm_provider=llm_provider, llm_secret=llm_secret
        )

        try:
            key = self.management_api.external_api_keys_api.api.update_external_api_key(
                account_id=account_id if account_id else self.account_id,
                external_key_id=external_key_id,
                external_api_key_modifiable=external_api_key_modifiable,
            )

            return ExternalAPIKey.model_validate(key.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

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
            If None, the account ID of the current instance is used.

        Examples
        --------
        >>> vantage_client = VantageClient()
        >>> vantage_client.delete_external_api_key(external_key_id="external_key_123")
        """

        try:
            self.management_api.external_api_keys_api.api.delete_external_api_key(
                account_id=account_id if account_id else self.account_id,
                external_key_id=external_key_id,
            )
        except Exception as exception:
            raise _parse_exception(exception)

    # endregion

    # region Collections

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
            If None, the account ID of the current instance is used.

        Returns
        -------
        List[Collection]
            A list of Collection objects, each representing a collection associated with the account.

        Examples
        --------
        >>> vantage_client = VantageClient(...)
        >>> collections = vantage_client.list_collections(account_id="12345")
        >>> for collection in collections:
        ...     print(collection.collection_name)
        "Collection 1"
        "Collection 2"
        """

        try:
            collections = (
                self.management_api.collection_api.api.list_collections(
                    account_id=account_id if account_id else self.account_id
                )
            )

            return [
                Collection.model_validate(
                    collection.actual_instance.model_dump()
                )
                for collection in collections
            ]
        except Exception as exception:
            raise _parse_exception(exception)

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
            If None, the account ID of the current instance is used.

        Returns
        -------
        List[str]
            A list of strings, each representing the unique ID of a collection associated with the account.
        """
        try:
            collections = self.list_collections(
                account_id=account_id if account_id else self.account_id
            )
            return [col.model_dump()["collection_id"] for col in collections]
        except Exception as exception:
            raise _parse_exception(exception)

    def create_collection(
        self,
        collection_id: str,
        collection_name: str,
        embeddings_dimension: int,
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
            If None, the current account ID is used.

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
        >>> print(new_collection.collection_id)
        "user-provided"

        Vantage-Managed:
        >>> vantage_client = VantageClient(...)
        >>> new_collection = vantage_client.create_collection(
                collection_id="vantage-managed",
                collection_name="My Collection",
                embeddings_dimension=1536,
                user_provided_embeddings=False,
            )
        >>> print(new_collection.collection_id)
        "vantage-managed"
        """

        if collection_id in self._existing_collection_ids(
            account_id=account_id
        ):
            raise VantageValueError(
                f"Collection with provided collection id [{collection_id}] already exists."  # noqa: E501
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

        try:
            collection = (
                self.management_api.collection_api.api.create_collection(
                    create_collection_request=create_collection_request,
                    account_id=account_id if account_id else self.account_id,
                )
            )

            return Collection.model_validate(collection.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

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
            If None, the current account ID is used.

        Returns
        -------
        Collection
            A Collection object containing the details of the specified collection.

        Example
        -------
        >>> vantage_client = VantageClient()
        >>> collection = vantage_client.get_collection(collection_id="unique_collection_id")
        >>> print(collection.collection_name)
        "My Collection"
        """

        if collection_id not in self._existing_collection_ids(
            account_id=account_id
        ):
            raise VantageNotFoundError(
                f"Collection with provided collection id [{collection_id}] does not exist."  # noqa: E501
            )

        try:
            collection = self.management_api.collection_api.api.get_collection(
                collection_id=collection_id,
                account_id=account_id if account_id else self.account_id,
            )

            return Collection.model_validate(collection.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

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
            If None, uses the current account ID.

        Returns
        -------
        Collection
            A Collection object representing the updated collection.

        Example
        -------
        >>> vantage_client = VantageClient()
        >>> updated_collection = vantage_client.update_collection(
                collection_id="my-collection",
                collection_name="Updated Collection Name",
            )
        >>> print(updated_collection.collection_name)
        "Updated Collection Name"
        """

        if collection_id not in self._existing_collection_ids(
            account_id=account_id
        ):
            raise VantageNotFoundError(
                f"Collection with provided collection id [{collection_id}] does not exist."  # noqa: E501
            )

        collection_modifiable = CollectionModifiable(
            external_key_id=external_key_id,
            collection_preview_url_pattern=collection_preview_url_pattern,
            collection_name=collection_name,
        )

        try:
            collection = (
                self.management_api.collection_api.api.update_collection(
                    collection_id=collection_id,
                    collection_modifiable=collection_modifiable,
                    account_id=account_id if account_id else self.account_id,
                )
            )

            return Collection.model_validate(collection.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

    def delete_collection(
        self,
        collection_id: str,
        account_id: Optional[str] = None,
    ) -> Collection:
        """
        Deletes a specific collection identified by its collection ID within a specified account. It first verifies
        the existence of the collection in the account and raises an exception if the collection does not exist. Upon
        successful deletion, it returns the Collection object that was deleted.

        Parameters
        ----------
        collection_id : str
            The unique identifier of the collection to be deleted.
        account_id : Optional[str], optional
            The account ID to which the collection belongs. If None, the current account ID is used.

        Returns
        -------
        Collection
            A Collection object representing the collection that was deleted.

        Example
        -------
        >>> vantage_client = VantageClient()
        >>> deleted_collection = vantage_client.delete_collection(collection_id="my-collection")
        """

        if collection_id not in self._existing_collection_ids(
            account_id=account_id
        ):
            raise VantageNotFoundError(
                f"Collection with provided collection id [{collection_id}] does not exist."  # noqa: E501
            )

        try:
            collection = (
                self.management_api.collection_api.api.delete_collection(
                    collection_id=collection_id,
                    account_id=account_id if account_id else self.account_id,
                )
            )

            return Collection.model_validate(collection.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

    def _get_browser_upload_url(
        self,
        collection_id: str,
        file_size: int,
        customer_batch_identifier: Optional[str] = None,
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
        customer_batch_identifier : Optional[str], optional
            An optional identifier provided by the customer to track the batch of uploads.
        account_id : Optional[str], optional
            The account ID to which the collection belongs. If None, the current account ID is used.

        Returns
        -------
        CollectionUploadURL
            An object containing the URL for browser-based file uploads.

        Raises
        ------
        VantageNotFoundError
            If the collection with the provided ID does not exist within the specified account.
        Exception
            For other exceptions that occur during the URL retrieval process.
        """

        if collection_id not in self._existing_collection_ids(
            account_id=account_id
        ):
            raise VantageNotFoundError(
                f"Collection with provided collection id [{collection_id}] does not exist."  # noqa: E501
            )

        try:
            url = (
                self.management_api.collection_api.api.get_browser_upload_url(
                    collection_id=collection_id,
                    file_size=file_size,
                    customer_batch_identifier=customer_batch_identifier,
                    account_id=account_id if account_id else self.account_id,
                )
            )

            return CollectionUploadURL.model_validate(url.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

    def upload_embedding(
        self,
        collection_id: str,
        content: bytes,
        file_size: int,
        customer_batch_identifier: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> int:
        browser_upload_url = self._get_browser_upload_url(
            collection_id=collection_id,
            file_size=file_size,
            customer_batch_identifier=customer_batch_identifier,
            account_id=account_id,
        )

        try:
            return self.management_api.collection_api.upload_embedding(
                upload_url=browser_upload_url.upload_url,
                upload_content=content,
            )
        except Exception as exception:
            raise _parse_exception(exception)

    def upload_embedding_by_path(
        self,
        collection_id: str,
        file_path: str,
        customer_batch_identifier: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> int:
        if not exists(file_path):
            raise FileNotFoundError(f"File \"{file_path}\" not found.")

        file_size = Path(file_path).stat().st_size
        file = open(file_path, "rb")
        file_content = file.read()
        return self.upload_embedding(
            collection_id=collection_id,
            content=file_content,
            file_size=file_size,
            customer_batch_identifier=customer_batch_identifier,
            account_id=account_id,
        )

    # endregion

    # region Search

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
        # TODO: docstring

        if collection_id not in self._existing_collection_ids(
            account_id=account_id
        ):
            raise VantageNotFoundError(
                f"Collection with provided collection id [{collection_id}] does not exist."  # noqa: E501
            )

        collection = GlobalSearchPropertiesCollection(
            collection_id=collection_id,
            accuracy=accuracy,
            account_id=account_id if account_id else self.account_id,
        )

        if page:
            pagination = GlobalSearchPropertiesPagination(
                page=page,
                count=page_count,
            )
        else:
            pagination = None

        if boolean_filter:
            search_filter = GlobalSearchPropertiesFilter(
                boolean_filter=boolean_filter,
            )
        else:
            search_filter = None

        query = EmbeddingSearchQuery(
            embedding=embedding,
            collection=collection,
            filter=search_filter,
            pagination=pagination,
        )

        vantage_api_key = (
            vantage_api_key if vantage_api_key else self.vantage_api_key
        )

        if not vantage_api_key:
            raise VantageValueError(
                "Vantage API Key is missing. Please provide the 'vantage_api_key' parameter to authenticate with the Search API."  # noqa: E501
            )

        try:
            result = self.search_api.api.embedding_search(
                query,
                _headers={"authorization": f"Bearer {vantage_api_key}"},
            )

            return SearchResult.model_validate(result.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

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
        # TODO: docstring

        if collection_id not in self._existing_collection_ids(account_id):
            raise VantageNotFoundError(
                f"Collection with provided collection id [{collection_id}] does not exist."  # noqa: E501
            )

        collection = GlobalSearchPropertiesCollection(
            collection_id=collection_id,
            accuracy=accuracy,
            account_id=account_id if account_id else self.account_id,
        )

        if page:
            pagination = GlobalSearchPropertiesPagination(
                page=page,
                count=page_count,
            )
        else:
            pagination = None

        if boolean_filter:
            search_filter = GlobalSearchPropertiesFilter(
                boolean_filter=boolean_filter,
            )
        else:
            search_filter = None

        query = SemanticSearchQuery(
            text=text,
            collection=collection,
            filter=search_filter,
            pagination=pagination,
        )

        vantage_api_key = (
            vantage_api_key if vantage_api_key else self.vantage_api_key
        )

        if not vantage_api_key:
            raise VantageValueError(
                "Vantage API Key is missing. Please provide the 'vantage_api_key' parameter to authenticate with the Search API."  # noqa: E501
            )

        try:
            result = self.search_api.api.semantic_search(
                query,
                _headers={"authorization": f"Bearer {vantage_api_key}"},
            )

            return SearchResult.model_validate(result.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

    def more_like_this_search(
        self,
        document_id: str,
        collection_id: Optional[str] = None,
        accuracy: Optional[int | float] = None,
        page: Optional[int] = None,
        page_count: Optional[int] = None,
        request_id: Optional[int] = None,
        boolean_filter: Optional[str] = None,
        account_id: Optional[str] = None,
        vantage_api_key: Optional[str] = None,
    ) -> SearchResult:
        # TODO: docstring

        if collection_id or accuracy:
            collection = GlobalSearchPropertiesCollection(
                account_id=(account_id if account_id else self.account_id),
                collection_id=collection_id,
                accuracy=accuracy,
            )
        else:
            collection = None

        if page:
            pagination = GlobalSearchPropertiesPagination(
                page=page,
                count=page_count,
            )
        else:
            pagination = None

        if boolean_filter:
            search_filter = GlobalSearchPropertiesFilter(
                boolean_filter=boolean_filter,
            )
        else:
            search_filter = None

        vantage_api_key = (
            vantage_api_key if vantage_api_key else self.vantage_api_key
        )

        if not vantage_api_key:
            raise VantageValueError(
                "Vantage API Key is missing. Please provide the 'vantage_api_key' parameter to authenticate with the Search API."  # noqa: E501
            )

        try:
            result = self.search_api.api.more_like_this_search(
                more_like_this_query=MoreLikeThisQuery(
                    collection=collection,
                    request_id=request_id,
                    filter=search_filter,
                    pagination=pagination,
                    document_id=document_id,
                ),
                _headers={"authorization": f"Bearer {vantage_api_key}"},
            )

            return SearchResult.model_validate(result.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

    def more_like_these_search(
        self,
        more_like_these: list[MoreLikeThese],
        collection_id: Optional[str] = None,
        accuracy: Optional[int | float] = None,
        page: Optional[int] = None,
        page_count: Optional[int] = None,
        request_id: Optional[int] = None,
        boolean_filter: Optional[str] = None,
        account_id: Optional[str] = None,
        vantage_api_key: Optional[str] = None,
    ) -> SearchResult:
        # TODO: docstring

        if collection_id or accuracy:
            collection = GlobalSearchPropertiesCollection(
                account_id=(account_id if account_id else self.account_id),
                collection_id=collection_id,
                accuracy=accuracy,
            )
        else:
            collection = None

        if page:
            pagination = GlobalSearchPropertiesPagination(
                page=page, count=page_count
            )
        else:
            pagination = None

        if boolean_filter:
            search_filter = GlobalSearchPropertiesFilter(
                boolean_filter=boolean_filter,
            )
        else:
            search_filter = None

        vantage_api_key = (
            vantage_api_key if vantage_api_key else self.vantage_api_key
        )

        if not vantage_api_key:
            raise VantageValueError(
                "Vantage API Key is missing. Please provide the 'vantage_api_key' parameter to authenticate with the Search API."  # noqa: E501
            )

        try:
            result = self.search_api.api.more_like_these_search(
                more_like_these_query=MoreLikeTheseQuery(
                    these=[
                        MLTheseTheseInner.model_validate(item.model_dump())
                        for item in more_like_these
                    ],
                    collection=collection,
                    request_id=request_id,
                    filter=search_filter,
                    pagination=pagination,
                ),
                _headers={"authorization": f"Bearer {vantage_api_key}"},
            )

            return SearchResult.model_validate(result.model_dump())
        except Exception as exception:
            raise _parse_exception(exception)

    # endregion

    # region Documents

    def upload_documents_from_jsonl(
        self,
        collection_id: str,
        documents: str,
        encoding: Optional[str] = None,
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
        encoding : Optional[str], optional
            The character encoding of the documents string. Currently not used.
        batch_identifier : Optional[str], optional
            An optional identifier provided by the user to track the batch of document uploads.
        account_id : Optional[str], optional
            The account ID to which the collection belongs.
            If None, the current account ID is used.

        Example
        -------
        >>> vantage_client = VantageClient()
        >>> documents_jsonl = '{"id": "1", "text": "Example text", "meta_color": "green", "meta_something": "value", "embeddings": [1,2,3, ...]}\\n{"id": "2", "text": "Lorem ipsum", "meta_color": "blue", "meta_something": "value", "embeddings": [4,5,6, ...]}'
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

        try:
            self.management_api.documents_api.api.upload_documents(
                body=documents,
                account_id=account_id if account_id else self.account_id,
                collection_id=collection_id,
                customer_batch_identifier=batch_identifier,
            )
        except Exception as exception:
            raise _parse_exception(exception)

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
            If None, the current account ID is used.

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
        {"id": "1", "text": "Example text", "meta_color": "green", "meta_something": "value", "embeddings": [1,2,3, ...]}


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
        )

    # endregion
