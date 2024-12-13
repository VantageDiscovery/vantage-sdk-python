from vantage_sdk.core.http.api.documents_api import DocumentsApi
from vantage_sdk.core.http.api_client import ApiClient


class DocumentsAPI:
    """
    Component for accessing documents part of search API.

    Attributes
    ----------
    api: DocumentsApi
        Component used to access the documents API.
    """

    def __init__(self, api_client: ApiClient):
        """
        Default constructor.

        Parameters
        ----------
        api_client: ApiClient
            Component used to make HTTP calls to the API.
        """
        self.api = DocumentsApi(api_client=api_client)
