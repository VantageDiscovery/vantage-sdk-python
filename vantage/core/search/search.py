from vantage.core.base import BaseAPI
from vantage.core.http.api.search_api import SearchApi


class SearchAPI(BaseAPI):
    def __init__(self, api_key: str, host: str | None):
        super().__init__(api_key, host)
        self.api = SearchApi(api_client=self.api_client)
