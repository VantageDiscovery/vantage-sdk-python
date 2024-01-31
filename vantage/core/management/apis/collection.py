import requests

from vantage.core.http.api import CollectionManagementApi
from vantage.core.http.api_client import ApiClient


class CollectionAPI:
    def __init__(self, api_client: ApiClient):
        self.api = CollectionManagementApi(api_client=api_client)

    def upload_embedding(self, upload_url: str, upload_content) -> int:
        response = requests.put(
            upload_url,
            data=upload_content,
        )

        return response.status_code
