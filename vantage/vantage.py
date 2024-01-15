from vantage.core.management import ManagementAPI
from vantage.core.search import SearchAPI

from vantage.core.http.models import Account

from typing import Optional

__all__ = ["Vantage"]


class Vantage:
    def __init__(
        self,
        vantage_api_key: str,
        management_api: Optional[ManagementAPI] = None,
        search_api: Optional[SearchAPI] = None,
    ) -> None:
        self.vantage_api_key = vantage_api_key

        if management_api:
            self.management_api = management_api
        else:
            self.management_api = ManagementAPI(self.vantage_api_key)

        if search_api:
            self.search_api = search_api
        else:
            self.search_api = SearchAPI(self.vantage_api_key)

    def account_info(self, account_id: str) -> Account:
        # TODO: docstring
        return self.management_api.account_api.account_info(account_id)
