from vantage.core.http.api.account_management_api import AccountManagementApi
from vantage.core.http.api_client import ApiClient


class AccountAPI:
    def __init__(self, api_client: ApiClient):
        self.api = AccountManagementApi(api_client=api_client)
