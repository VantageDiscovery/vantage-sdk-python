from __future__ import annotations

from typing import Optional

from vantage.core.base import AuthorizationClient
from vantage.core.http.models import User
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
        vantage_api_key = auth_client.jwt_token
        management_api = ManagementAPI.from_defaults(vantage_api_key, host)
        search_api = SearchAPI(vantage_api_key, host)
        return cls(vantage_api_key, management_api, search_api, host)

    def logged_in_user(self) -> User:
        # TODO: docstring
        return self.management_api.account_api.api.user_me()
