from vantage.core.base import BaseAPI
from vantage.core.http.api.search_api import SearchApi
from vantage.core.http.models import (
    EmbeddingSearchQueryFull,
    SearchResult,
    SemanticSearchQueryFull,
)


__all__ = ["SearchAPI"]


class SearchAPI(BaseAPI):
    def __init__(self, api_key: str, host: str | None):
        super().__init__(api_key, host)
        self.api = SearchApi()

    def semantic_search(self, query: SemanticSearchQueryFull) -> SearchResult:
        # TODO: docstring
        return self.api.semantic_search(semantic_search_query_full=query)

    def embedding_search(
        self, query: EmbeddingSearchQueryFull
    ) -> SearchResult:
        # TODO: docstring
        return self.api.embedding_search(
            self, embedding_search_query_full=query
        )
