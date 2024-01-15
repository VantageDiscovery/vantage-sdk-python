from vantage.core.http.api.search_api import SearchApi
from vantage.core.http.models import (
    SemanticSearchQueryFull,
    SearchResult,
    EmbeddingSearchQueryFull,
)
from vantage.core.base import BaseAPI

__all__ = ["SearchAPI"]


class SearchAPI(BaseAPI):
    def semantic_search(self, query: SemanticSearchQueryFull) -> SearchResult:
        # TODO: docstring
        return SearchApi.semantic_search(semantic_search_query_full=query)

    def embedding_search(
        self, query: EmbeddingSearchQueryFull
    ) -> SearchResult:
        # TODO: docstring
        return SearchApi.embedding_search(
            self, embedding_search_query_full=query
        )
