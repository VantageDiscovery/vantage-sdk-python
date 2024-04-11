"""Top-level package for Vantage SDK Python."""

from vantage_sdk.model.account import Account
from vantage_sdk.model.collection import Collection, CollectionUploadURL
from vantage_sdk.model.keys import ExternalAPIKey, VantageAPIKey
from vantage_sdk.model.search import (
    MoreLikeTheseItem,
    SearchResult,
    SearchResultItem,
)
from vantage_sdk.vantage_sdk import VantageClient


__author__ = """Vantage"""
__email__ = 'none@vantage.com'
__version__ = '0.0.13'
__all__ = [
    "VantageClient",
    "Collection",
    "CollectionUploadURL",
    "Account",
    "VantageAPIKey",
    "ExternalAPIKey",
    "SearchResult",
    "SearchResultItem",
    "MoreLikeTheseItem",
]
