from vantage.core.http.api.search_api import SearchApi
from vantage.core.http.api_client import ApiClient


class SearchAPI:
    def __init__(self, api_client: ApiClient):
        self.api = SearchApi(api_client=api_client)
