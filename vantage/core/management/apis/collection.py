from vantage.core.base import BaseAPI
from vantage.core.http.api import CollectionManagementApi


__all__ = ["CollectionAPI"]


class CollectionAPI(BaseAPI):
    def __init__(self, api_key: str, host: str | None):
        super().__init__(api_key, host)
        self.api = CollectionManagementApi()
