from __future__ import annotations

from typing import Optional

from vantage.core.base import AuthorizationClient, AuthorizedApiClient
from vantage.core.http.models import (
    Account,
    AccountModifiable,
    Collection,
    CollectionModifiable,
    CollectionsResult,
    CreateCollectionRequest,
    User,
    UserModifiable,
    UserRegistrationFields,
)
from vantage.core.management import ManagementAPI
from vantage.core.search import SearchAPI


class Vantage:
    def __init__(
        self,
        vantage_api_key: str,
        management_api: ManagementAPI,
        search_api: SearchAPI,
        host: Optional[str] = None,
    ) -> None:
        self.vantage_api_key = vantage_api_key
        self.management_api = management_api
        self.search_api = search_api
        self.host = host

    @classmethod
    def from_defaults(
        cls,
        vantage_client_id: str,
        vantage_client_secret: str,
        host: Optional[str] = None,
    ) -> Vantage:
        auth_client = AuthorizationClient(
            vantage_client_id=vantage_client_id,
            vantage_client_secret=vantage_client_secret,
        )
        auth_client.authenticate()
        api_client = AuthorizedApiClient(
            pool_threads=1, authorization_client=auth_client
        )
        vantage_api_key = auth_client.jwt_token
        management_api = ManagementAPI.from_defaults(api_client)
        search_api = SearchAPI(api_client)

        return cls(vantage_api_key, management_api, search_api, host)

    def logged_in_user(self) -> User:
        # TODO: docstring
        return self.management_api.account_api.api.user_me()

    # TODO: Check what fields are mandatory
    def register_user(
        self,
        user_given_name: Optional[str] = None,
        user_family_name: Optional[str] = None,
        user_email: Optional[str] = None,
        user_last_login_date: Optional[str] = None,
        info_regform_company_name: Optional[str] = None,
        info_regform_company_industry: Optional[str] = None,
        info_regform_company_use_case: Optional[str] = None,
        info_signed_jwt_from_provider: Optional[str] = None,
    ) -> User:
        data = UserRegistrationFields(
            user_given_name=user_given_name,
            user_family_name=user_family_name,
            user_email=user_email,
            user_last_login_date=user_last_login_date,
            info_regform_company_name=info_regform_company_name,
            info_regform_company_industry=info_regform_company_industry,
            info_regform_company_use_case=info_regform_company_use_case,
            info_signed_jwt_from_provider=info_signed_jwt_from_provider,
        )
        return self.management_api.account_api.api.register_user(data)

    def get_user(self, user_id: str) -> User:
        return self.management_api.account_api.api.get_user(user_id)

    # TODO: Check what fields are mandatory
    def update_user(
        self,
        user_id: str,
        user_given_name: Optional[str] = None,
        user_family_name: Optional[str] = None,
        user_email: Optional[str] = None,
        user_last_login_date: Optional[str] = None,
    ) -> User:
        data = UserModifiable(
            user_given_name=user_given_name,
            user_family_name=user_family_name,
            user_email=user_email,
            user_last_login_date=user_last_login_date,
        )
        return self.management_api.account_api.api.update_user(user_id, data)

    def get_account(self, account_id: str) -> Account:
        return self.management_api.account_api.api.get_account(account_id)

    # TODO: Check what fields are mandatory
    def update_account(
        self, account_id: str, account_name: Optional[str] = None
    ) -> Account:
        data = AccountModifiable(account_name=account_name)
        return self.management_api.account_api.api.update_account(
            account_id, data
        )

    # region Collections

    def list_collections(self, account_id: str) -> CollectionsResult:
        # TODO: docstring

        # TODO: check error -> expected dict not list in CollectionsResult

        return self.management_api.collection_api.api.list_collections(
            account_id
        )

    def create_collection(
        self,
        account_id: str,
        collection_id: str,
        collection_name: str,
        embeddings_dimension: int,
        user_provided_embeddings: Optional[bool] = False,
        llm_provider: Optional[str] = None,
        llm_model: Optional[str] = None,
        external_key_id: Optional[str] = None,
        collection_preview_url_pattern: Optional[str] = None,
    ) -> Collection:
        # TODO: docstring

        # Note: Only scenario for user provided embeddings is covered
        # TODO: check if collection exists
        # TODO: two cases -> user provided embeddings or not

        create_collection_request = CreateCollectionRequest(
            external_key_id=external_key_id,
            collection_id=collection_id,
            collection_name=collection_name,
            embeddings_dimension=int(embeddings_dimension),
            user_provided_embeddings=bool(user_provided_embeddings),
            collection_preview_url_pattern=collection_preview_url_pattern,
        )

        return self.management_api.collection_api.api.create_collection(
            account_id, create_collection_request
        )

    def get_collection(
        self,
        collection_id: str,
        account_id: str,
    ) -> Collection:
        # TODO: docstring

        # TODO: check if exists

        return self.management_api.collection_api.api.get_collection(
            collection_id=collection_id, account_id=account_id
        )

    def update_collection(
        self,
        collection_id: str,
        account_id: str,
        collection_name: Optional[str] = None,
        external_key_id: Optional[str] = None,
        collection_preview_url_pattern: Optional[str] = None,
    ) -> Collection:
        # TODO: docstring

        # TODO: check if exists

        collection_modifiable = CollectionModifiable(
            external_key_id=external_key_id,
            collection_preview_url_pattern=collection_preview_url_pattern,
            collection_name=collection_name,
        )

        return self.management_api.collection_api.api.update_collection(
            collection_id=collection_id,
            account_id=account_id,
            collection_modifiable=collection_modifiable,
        )

    def delete_collection(
        self,
        collection_id: str,
        account_id: str,
    ) -> Collection:
        # TODO: docstring

        # TODO: check if exists (Note: if not -> 503 -> inform)

        return self.management_api.collection_api.api.delete_collection(
            collection_id=collection_id, account_id=account_id
        )

    # endregion
