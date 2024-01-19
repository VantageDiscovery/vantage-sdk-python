from vantage.core.base import BaseAPI
from vantage.core.http.api.account_management_api import AccountManagementApi


class AccountAPI(BaseAPI):
    def __init__(
        self, api_key: str, host: str | None, pool_threads: int | None = 1
    ):
        super().__init__(api_key, host, pool_threads)
        self.api = AccountManagementApi(api_client=self.api_client)
