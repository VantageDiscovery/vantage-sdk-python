"""Top-level package for Vantage SDK Python."""

from vantage.vantage import VantageClient
from vantage.model.collection import Collection, CollectionUploadURL
from vantage.model.account import Account
from vantage.model.keys import VantageAPIKey, ExternalAPIKey
from vantage.model.search import SearchResult, SearchResultItem, MoreLikeThese


__author__ = """Vantage"""
__email__ = 'none@vantage.com'
__version__ = '0.0.6'
__all__ = [
    "VantageClient",
    "Collection",
    "CollectionUploadURL",
    "Account",
    "VantageAPIKey",
    "ExternalAPIKey",
    "SearchResult",
    "SearchResultItem",
    "MoreLikeThese",
]
