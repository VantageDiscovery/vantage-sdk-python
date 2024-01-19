from __future__ import annotations

from typing import Optional

from vantage.core.http.models import Account
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
        cls, vantage_api_key: str, host: Optional[str] = None
    ) -> Vantage:
        management_api = ManagementAPI.from_defaults(vantage_api_key, host)
        search_api = SearchAPI(vantage_api_key, host)
        return cls(vantage_api_key, management_api, search_api, host)

    def logged_in_user(self) -> Account:
        # TODO: docstring
        return self.management_api.account_api.api.user_me()
