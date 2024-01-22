from vantage.core.http.api.vantage_api_keys_api import VantageAPIKeysApi
from vantage.core.http.api_client import ApiClient


class VantageAPIKeysAPI:
    def __init__(self, api_client: ApiClient):
        self.api = VantageAPIKeysApi(api_client=api_client)
