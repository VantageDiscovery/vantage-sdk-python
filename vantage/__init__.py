"""Top-level package for Vantage SDK Python."""

from vantage.model.account import Account
from vantage.model.collection import Collection, CollectionUploadURL
from vantage.model.keys import ExternalAPIKey, VantageAPIKey
from vantage.model.search import (
    MoreLikeTheseItem,
    SearchResult,
    SearchResultItem,
)
from vantage.vantage import VantageClient


__author__ = """Vantage"""
__email__ = 'none@vantage.com'
__version__ = '0.0.11'
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
