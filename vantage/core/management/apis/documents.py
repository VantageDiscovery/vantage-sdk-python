from vantage.core.http.api.documents_api import DocumentsApi
from vantage.core.http.api_client import ApiClient


class DocumentsAPI:
    def __init__(self, api_client: ApiClient):
        self.api = DocumentsApi(api_client=api_client)
