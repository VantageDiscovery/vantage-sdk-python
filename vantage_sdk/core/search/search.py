"""This module contains SearchAPI, a class for accessing search API."""

from vantage_sdk.core.http.api.search_api import SearchApi
from vantage_sdk.core.http.api_client import ApiClient


class SearchAPI:
    """
    Component for accessing the search API.

    Attributes
    ----------
    api: SearchApi
        Component used to access the search API.
    """

    def __init__(self, api_client: ApiClient):
        """
        Default constructor.

        Parameters
        ----------
        api_client: ApiClient
            Component used to make HTTP calls to the API.
        """
        self.api = SearchApi(api_client=api_client)
