from typing import Optional

from vantage.core.http.models import Account
from vantage.core.management import ManagementAPI
from vantage.core.search import SearchAPI


__all__ = ["Vantage"]


class Vantage:
    def __init__(
        self,
        vantage_api_key: str,
        host: Optional[str] = None,
        management_api: Optional[ManagementAPI] = None,
        search_api: Optional[SearchAPI] = None,
    ) -> None:
        self.vantage_api_key = vantage_api_key

        if management_api:
            self.management_api = management_api
        else:
            self.management_api = ManagementAPI(self.vantage_api_key, host)

        if search_api:
            self.search_api = search_api
        else:
            self.search_api = SearchAPI(self.vantage_api_key, host)

    def logged_in_user(self) -> Account:
        # TODO: docstring
        return self.management_api.account_api.logged_in_user()
