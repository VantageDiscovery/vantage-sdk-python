from __future__ import annotations

from os.path import exists
from pathlib import Path
from typing import List, Optional

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
from vantage.exceptions import VantageNotFoundException, VantageValueError
from vantage.model.account import Account
from vantage.model.collection import Collection, CollectionUploadURL
from vantage.model.keys import ExternalAPIKey, VantageAPIKey
from vantage.model.search import MoreLikeThese, SearchResult


class Vantage:
    def __init__(
        self,
        management_api: ManagementAPI,
        search_api: SearchAPI,
        account_id: str,
        vantage_api_key: Optional[str] = None,
        host: Optional[str] = None,
    ) -> None:
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
    ) -> Vantage:
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
    ) -> Vantage:
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
        # TODO: docstring

        result = self.management_api.account_api.api.get_account(
            account_id=account_id if account_id else self.account_id
        )
        return Account.parse_obj(result.model_dump())

    # TODO: Check what fields are mandatory
    def update_account(
        self,
        account_name: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> Account:
        # TODO: docstring

        account_modifiable = AccountModifiable(account_name=account_name)

        return self.management_api.account_api.api.update_account(
            account_id=account_id if account_id else self.account_id,
            account_modifiable=account_modifiable,
        )

    # endregion

    # region Vantage API keys

    def get_vantage_api_keys(
        self,
        account_id: Optional[str] = None,
    ) -> List[VantageAPIKey]:
        # TODO: docstring

        keys = (
            self.management_api.vantage_api_keys_api.api.get_vantage_api_keys(
                account_id=account_id if account_id else self.account_id,
            )
        )
        return [
            VantageAPIKey.parse_obj(key.actual_instance.model_dump())
            for key in keys
        ]

    def get_vantage_api_key(
        self,
        vantage_api_key_id: str,
        account_id: Optional[str] = None,
    ) -> VantageAPIKey:
        # TODO: docstring

        key = self.management_api.vantage_api_keys_api.api.get_vantage_api_key(
            account_id=account_id if account_id else self.account_id,
            vantage_api_key_id=vantage_api_key_id,
        )
        return VantageAPIKey.parse_obj(key.model_dump())

    # endregion

    # region External API keys

    def create_external_api_key(
        self,
        url: str,
        llm_provider: str,
        llm_secret: str,
        account_id: Optional[str] = None,
    ) -> ExternalAPIKey:
        # TODO: docstring

        external_api_key_modifiable = ExternalAPIKeyModifiable(
            url=url, llm_provider=llm_provider, llm_secret=llm_secret
        )

        key = self.management_api.external_api_keys_api.api.create_external_api_key(
            account_id=account_id if account_id else self.account_id,
            external_api_key_modifiable=external_api_key_modifiable,
        )

        return ExternalAPIKey.parse_obj(key.model_dump())

    def get_external_api_keys(
        self,
        account_id: Optional[str] = None,
    ) -> List[ExternalAPIKey]:
        # TODO: docstring

        keys = self.management_api.external_api_keys_api.api.get_external_api_keys(
            account_id=account_id if account_id else self.account_id,
        )

        return [
            ExternalAPIKey.parse_obj(key.actual_instance.model_dump())
            for key in keys
        ]

    def get_external_api_key(
        self,
        external_key_id: str,
        account_id: Optional[str] = None,
    ) -> ExternalAPIKey:
        # TODO: docstring

        key = (
            self.management_api.external_api_keys_api.api.get_external_api_key(
                account_id=account_id if account_id else self.account_id,
                external_key_id=external_key_id,
            )
        )

        return ExternalAPIKey.parse_obj(key.model_dump())

    def update_external_api_key(
        self,
        external_key_id: str,
        url: str,
        llm_provider: str,
        llm_secret: str,
        account_id: Optional[str] = None,
    ) -> ExternalAPIKey:
        # TODO: docstring

        external_api_key_modifiable = ExternalAPIKeyModifiable(
            url=url, llm_provider=llm_provider, llm_secret=llm_secret
        )

        key = self.management_api.external_api_keys_api.api.update_external_api_key(
            account_id=account_id if account_id else self.account_id,
            external_key_id=external_key_id,
            external_api_key_modifiable=external_api_key_modifiable,
        )

        return ExternalAPIKey.parse_obj(key.model_dump())

    def delete_external_api_key(
        self,
        external_key_id: str,
        account_id: Optional[str] = None,
    ) -> None:
        # TODO: docstring

        self.management_api.external_api_keys_api.api.delete_external_api_key(
            account_id=account_id if account_id else self.account_id,
            external_key_id=external_key_id,
        )

    # endregion

    # region Collections

    def list_collections(
        self,
        account_id: Optional[str] = None,
    ) -> List[Collection]:
        # TODO: docstring

        collections = self.management_api.collection_api.api.list_collections(
            account_id=account_id if account_id else self.account_id
        )

        return [
            Collection.parse_obj(collection.actual_instance.model_dump())
            for collection in collections
        ]

    def _existing_collection_ids(
        self,
        account_id: Optional[str] = None,
    ) -> List[str]:
        collections = self.list_collections(
            account_id=account_id if account_id else self.account_id
        )
        return [col.model_dump()["collection_id"] for col in collections]

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
        # TODO: docstring

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

        collection = self.management_api.collection_api.api.create_collection(
            create_collection_request=create_collection_request,
            account_id=account_id if account_id else self.account_id,
        )

        return Collection.parse_obj(collection.model_dump())

    def get_collection(
        self,
        collection_id: str,
        account_id: Optional[str] = None,
    ) -> Collection:
        # TODO: docstring

        if collection_id not in self._existing_collection_ids(
            account_id=account_id
        ):
            raise VantageNotFoundException(
                f"Collection with provided collection id [{collection_id}] does not exist."  # noqa: E501
            )

        collection = self.management_api.collection_api.api.get_collection(
            collection_id=collection_id,
            account_id=account_id if account_id else self.account_id,
        )

        return Collection.parse_obj(collection.model_dump())

    def update_collection(
        self,
        collection_id: str,
        collection_name: Optional[str] = None,
        external_key_id: Optional[str] = None,
        collection_preview_url_pattern: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> Collection:
        # TODO: docstring

        if collection_id not in self._existing_collection_ids(
            account_id=account_id
        ):
            raise VantageNotFoundException(
                f"Collection with provided collection id [{collection_id}] does not exist."  # noqa: E501
            )

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

        return Collection.parse_obj(collection.model_dump())

    def delete_collection(
        self,
        collection_id: str,
        account_id: Optional[str] = None,
    ) -> Collection:
        # TODO: docstring

        if collection_id not in self._existing_collection_ids(
            account_id=account_id
        ):
            raise VantageNotFoundException(
                f"Collection with provided collection id [{collection_id}] does not exist."  # noqa: E501
            )

        collection = self.management_api.collection_api.api.delete_collection(
            collection_id=collection_id,
            account_id=account_id if account_id else self.account_id,
        )

        return Collection.parse_obj(collection.model_dump())

    def _get_browser_upload_url(
        self,
        collection_id: str,
        file_size: int,
        customer_batch_identifier: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> CollectionUploadURL:
        # TODO: docstring

        if collection_id not in self._existing_collection_ids(
            account_id=account_id
        ):
            raise VantageNotFoundException(
                f"Collection with provided collection id [{collection_id}] does not exist."  # noqa: E501
            )

        url = self.management_api.collection_api.api.get_browser_upload_url(
            collection_id=collection_id,
            file_size=file_size,
            customer_batch_identifier=customer_batch_identifier,
            account_id=account_id if account_id else self.account_id,
        )

        return CollectionUploadURL.parse_obj(url.model_dump())

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
        return self.management_api.collection_api.upload_embedding(
            upload_url=browser_upload_url.upload_url,
            upload_content=content,
        )

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
        vantage_api_key: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> SearchResult:
        # TODO: docstring

        if collection_id not in self._existing_collection_ids(
            account_id=account_id
        ):
            raise VantageNotFoundException(
                f"Collection with provided collection id [{collection_id}] does not exist."  # noqa: E501
            )

        collection = GlobalSearchPropertiesCollection(
            collection_id=collection_id,
            accuracy=accuracy,
            account_id=account_id if account_id else self.account_id,
        )

        query = EmbeddingSearchQuery(
            embedding=embedding,
            collection=collection,
            filter=None,
            pagination=None,
        )

        vantage_api_key = (
            vantage_api_key if vantage_api_key else self.vantage_api_key
        )

        if not vantage_api_key:
            raise VantageValueError(
                "Vantage API Key is missing. Please provide the 'vantage_api_key' parameter to authenticate with the Search API."  # noqa: E501
            )

        result = self.search_api.api.embedding_search(
            query,
            _headers={"authorization": f"Bearer {vantage_api_key}"},
        )

        return SearchResult.parse_obj(result.model_dump())

    def semantic_search(
        self,
        text: str,
        collection_id: str,
        accuracy: float = 0.3,
        vantage_api_key: Optional[str] = None,
        account_id: Optional[str] = None,
    ) -> SearchResult:
        # TODO: docstring

        if collection_id not in self._existing_collection_ids(account_id):
            raise VantageNotFoundException(
                f"Collection with provided collection id [{collection_id}] does not exist."  # noqa: E501
            )

        collection = GlobalSearchPropertiesCollection(
            collection_id=collection_id,
            accuracy=accuracy,
            account_id=account_id if account_id else self.account_id,
        )

        query = SemanticSearchQuery(
            text=text,
            collection=collection,
            filter=None,
            pagination=None,
        )

        vantage_api_key = (
            vantage_api_key if vantage_api_key else self.vantage_api_key
        )

        if not vantage_api_key:
            raise VantageValueError(
                "Vantage API Key is missing. Please provide the 'vantage_api_key' parameter to authenticate with the Search API."  # noqa: E501
            )

        result = self.search_api.api.semantic_search(
            query,
            _headers={"authorization": f"Bearer {vantage_api_key}"},
        )

        return SearchResult.parse_obj(result.model_dump())

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
                page=page, count=page_count
            )
        else:
            pagination = None

        if boolean_filter:
            search_filter = GlobalSearchPropertiesFilter(boolean_filter="")
        else:
            search_filter = None

        vantage_api_key = (
            vantage_api_key if vantage_api_key else self.vantage_api_key
        )

        if not vantage_api_key:
            raise VantageValueError(
                "Vantage API Key is missing. Please provide the 'vantage_api_key' parameter to authenticate with the Search API."  # noqa: E501
            )

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

        return SearchResult.parse_obj(result.model_dump())

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
            search_filter = GlobalSearchPropertiesFilter(boolean_filter="")
        else:
            search_filter = None

        vantage_api_key = (
            vantage_api_key if vantage_api_key else self.vantage_api_key
        )

        if not vantage_api_key:
            raise VantageValueError(
                "Vantage API Key is missing. Please provide the 'vantage_api_key' parameter to authenticate with the Search API."  # noqa: E501
            )

        result = self.search_api.api.more_like_these_search(
            more_like_these_query=MoreLikeTheseQuery(
                these=[
                    MLTheseTheseInner.parse_obj(item.model_dump())
                    for item in more_like_these
                ],
                collection=collection,
                request_id=request_id,
                filter=search_filter,
                pagination=pagination,
            ),
            _headers={"authorization": f"Bearer {vantage_api_key}"},
        )

        return SearchResult.parse_obj(result.model_dump())

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
        # TODO: docstring

        aid = account_id if account_id else self.account_id
        self.management_api.documents_api.api.upload_documents(
            body=documents,
            account_id=aid,
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
