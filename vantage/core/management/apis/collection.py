from vantage.core.http.api import CollectionManagementApi
from vantage.core.http.api_client import ApiClient


class CollectionAPI:
    def __init__(self, api_client: ApiClient):
        self.api = CollectionManagementApi(api_client=api_client)
