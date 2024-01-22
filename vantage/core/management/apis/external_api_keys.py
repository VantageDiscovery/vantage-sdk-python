from vantage.core.http.api.external_api_keys_api import ExternalAPIKeysApi
from vantage.core.http.api_client import ApiClient


class ExternalAPIKeysAPI:
    def __init__(self, api_client: ApiClient):
        self.api = ExternalAPIKeysApi(api_client=api_client)
