import requests

from vantage.core.http.api import CollectionManagementApi
from vantage.core.http.api_client import ApiClient
from vantage.exceptions import VantageFileUploadException


class CollectionAPI:
    def __init__(self, api_client: ApiClient):
        self.api = CollectionManagementApi(api_client=api_client)

    def upload_embedding(self, upload_url: str, upload_content) -> int:
        response = requests.put(
            upload_url,
            data=upload_content,
        )

        if response.status_code != 200:
            raise VantageFileUploadException(
                response.reason, response.status_code
            )

        return response.status_code
