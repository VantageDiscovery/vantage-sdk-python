#!/usr/bin/env python

import pytest

from vantage_sdk.client import VantageClient
from vantage_sdk.core.http.exceptions import (
    BadRequestException,
    UnauthorizedException,
)
from vantage_sdk.model.search import (
    Facet,
    FacetType,
    Filter,
    MoreLikeTheseItem,
)


"""Integration tests for search endpoints"""


class TestSearch:
    def test_if_embedding_search_returns_result(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if embedding search will return correct result.
        """
        # Given
        collection_id = test_collection_id
        search_embedding = [1, 1, 1, 1, 1]

        # When
        result = client.embedding_search(
            embedding=search_embedding,
            collection_id=collection_id,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 200
        assert len(result.results) == 10

    def test_embedding_search_on_non_existing_collection(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if searching a non-existing collection will raise an exception.
        """
        # Given
        collection_id = test_collection_id
        search_embedding = [1, 1, 1, 1, 1]

        # When
        with pytest.raises(UnauthorizedException) as exception:
            client.embedding_search(
                embedding=search_embedding,
                collection_id=collection_id,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is UnauthorizedException

    def test_embedding_search_with_invalid_embedding(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if searching using an empty embedding will raise an exception.
        """
        # Given
        collection_id = test_collection_id
        search_embedding = []

        # When
        with pytest.raises(BadRequestException) as exception:
            client.embedding_search(
                embedding=search_embedding,
                collection_id=collection_id,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is BadRequestException

    def test_embedding_search_with_invalid_accuracy(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if searching using invalid accuracy parameter
        will raise an exception.
        """
        # Given
        collection_id = test_collection_id
        search_embedding = [1, 1, 1, 1, 1]
        accuracy = 800

        # When
        with pytest.raises(BadRequestException) as exception:
            client.embedding_search(
                embedding=search_embedding,
                collection_id=collection_id,
                accuracy=accuracy,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is BadRequestException

    def test_if_semantic_search_returns_result(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if semantic search will return correct result.
        """
        # Given
        collection_id = test_collection_id
        accuracy = 0.2
        search_text = "short legs and long body"

        # When
        result = client.semantic_search(
            text=search_text,
            collection_id=collection_id,
            accuracy=accuracy,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 200
        assert len(result.results) == 10

    def test_semantic_search_on_non_existing_collection(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if performing a semantic search on an non-existing collection
        will raise an exception.
        """
        # Given
        collection_id = test_collection_id
        search_text = "Test search"

        # When
        with pytest.raises(UnauthorizedException) as exception:
            client.semantic_search(
                text=search_text,
                collection_id=collection_id,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is UnauthorizedException

    def test_semantic_search_with_invalid_accuracy(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if performing a semantic search with an invalid
        accuracy parameter will raise an exception.
        """

        # Given
        collection_id = test_collection_id
        search_text = "Test search"
        accuracy = 800

        # When
        with pytest.raises(BadRequestException) as exception:
            client.semantic_search(
                text=search_text,
                collection_id=collection_id,
                accuracy=accuracy,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is BadRequestException

    def test_more_like_this_search(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ) -> None:
        """
        Tests if MoreLikeThis search will return correct result.
        """
        # Given
        collection_id = test_collection_id
        expected_results = {
            "en_0370917": {"score": 0.907},
            'en_0127807': {"score": 0.904},
            'en_0772990': {"score": 0.904},
        }

        # When
        response = client.more_like_this_search(
            collection_id=collection_id,
            document_id="en_0530926",
            account_id=account_params["id"],
        )

        # Then
        assert response is not None
        assert response.status == 200
        results = response.results
        assert len(results) == len(expected_results)
        for result in results:
            assert result.id in expected_results.keys()
            assert expected_results[result.id]["score"] == round(
                result.score, 3
            )

    def test_more_like_these_search(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ) -> None:
        """
        Tests if MoreLikeThese search will return correct result.
        """
        # Given
        collection_id = test_collection_id
        more_like_these = [
            MoreLikeTheseItem(
                weight=1.0,
                query_text="some text",
            ),
            MoreLikeTheseItem(
                weight=1.0,
                query_text="other text",
            ),
        ]
        expected_results = {
            "en_0022659": {"score": 0.891},
            "en_0375881": {"score": 0.891},
            "en_0266579": {"score": 0.891},
            "en_0218966": {"score": 0.891},
            "en_0622322": {"score": 0.89},
        }

        response = client.more_like_these_search(
            collection_id=collection_id,
            account_id=account_params["id"],
            more_like_these=more_like_these,
        )

        # Then
        assert response is not None
        assert response.status == 200
        results = response.results
        assert len(results) == len(expected_results)
        for result in results:
            assert result.id in expected_results.keys()
            assert expected_results[result.id]["score"] == round(
                result.score, 3
            )

    # region Variants

    def test_semantic_search_with_variant_filter(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if semantic search will return correct result using variant filter option.
        """
        # Given
        collection_id = test_collection_id
        search_text = "Test search"

        filter = Filter(
            variant_filter="(color:\"black\" OR color:\"brown\")",
        )

        # When
        result = client.semantic_search(
            text=search_text,
            collection_id=collection_id,
            filter=filter,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 200
        assert len(result.results) == 3
        for r in result.results:
            assert "variants" in r.model_dump().keys()
        for r in result.results:
            assert "variants_full_list" in r.model_dump().keys()

    def test_embedding_search_with_variant_filter(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if embedding search will return correct result using variant filter option.
        """
        # Given
        collection_id = test_collection_id
        embedding = [1, 1, 1, 1, 1]

        filter = Filter(
            variant_filter="(color:\"black\" OR color:\"brown\")",
        )

        # When
        result = client.embedding_search(
            embedding=embedding,
            collection_id=collection_id,
            filter=filter,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 200
        assert len(result.results) == 3
        for r in result.results:
            assert "variants" in r.model_dump().keys()
        for r in result.results:
            assert "variants_full_list" in r.model_dump().keys()

    def test_more_like_this_search_with_variant_filter(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if MoreLikeThis search will return correct result using variant filter option.
        """
        # Given
        collection_id = test_collection_id
        document_id = "en_0530926"

        filter = Filter(
            variant_filter="(color:\"black\" OR color:\"brown\")",
        )

        # When
        result = client.more_like_this_search(
            document_id=document_id,
            collection_id=collection_id,
            filter=filter,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 200
        assert len(result.results) == 3
        for r in result.results:
            assert "variants" in r.model_dump().keys()
        for r in result.results:
            assert "variants_full_list" in r.model_dump().keys()

    def test_more_like_these_search_with_variant_filter(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if MoreLikeThese search will return correct result using variant filter option.
        """
        # Given
        collection_id = test_collection_id
        these = [
            MoreLikeTheseItem(
                weight=1.0,
                query_text="some text",
            ),
            MoreLikeTheseItem(
                weight=1.0,
                query_text="other text",
            ),
        ]

        filter = Filter(
            variant_filter="(color:\"black\" OR color:\"brown\")",
        )

        # When
        result = client.more_like_these_search(
            more_like_these=these,
            collection_id=collection_id,
            filter=filter,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 200
        assert len(result.results) == 3
        for r in result.results:
            assert "variants" in r.model_dump().keys()
        for r in result.results:
            assert "variants_full_list" in r.model_dump().keys()

    # endregion

    # region Facets

    def test_semantic_search_with_facets(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if semantic search will return correct result with facets.
        """
        # Given
        collection_id = test_collection_id
        search_text = "Test search"

        facets = [
            Facet(
                name="color",
                type=FacetType.COUNT,
            ),
            Facet(
                name="size",
                type=FacetType.COUNT,
                values=["sm", "md"],
            ),
        ]

        # When
        result = client.semantic_search(
            text=search_text,
            collection_id=collection_id,
            facets=facets,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 200
        assert len(result.results) == 3
        assert len(result.facets) == len(facets)

    def test_embedding_search_with_facets(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if embedding search will return correct result with facets.
        """
        # Given
        collection_id = test_collection_id
        embedding = [1, 1, 1, 1, 1]

        facets = [
            Facet(
                name="color",
                type=FacetType.COUNT,
            ),
            Facet(
                name="size",
                type=FacetType.COUNT,
                values=["sm", "md"],
            ),
        ]

        # When
        result = client.embedding_search(
            embedding=embedding,
            collection_id=collection_id,
            facets=facets,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 200
        assert len(result.results) == 3
        assert len(result.facets) == len(facets)

    def test_more_like_this_search_with_facets(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if MoreLikeThis search will return correct result with facets.
        """
        # Given
        collection_id = test_collection_id
        document_id = "en_0530926"

        facets = [
            Facet(
                name="color",
                type=FacetType.COUNT,
            ),
            Facet(
                name="size",
                type=FacetType.COUNT,
                values=["sm", "md"],
            ),
        ]

        # When
        result = client.more_like_this_search(
            document_id=document_id,
            collection_id=collection_id,
            facets=facets,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 200
        assert len(result.results) == 3
        assert len(result.facets) == len(facets)

    def test_more_like_these_search_with_facets(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if MoreLikeThese search will return correct result with facets.
        """
        # Given
        collection_id = test_collection_id
        these = [
            MoreLikeTheseItem(
                weight=1.0,
                query_text="some text",
            ),
            MoreLikeTheseItem(
                weight=1.0,
                query_text="other text",
            ),
        ]

        facets = [
            Facet(
                name="color",
                type=FacetType.COUNT,
            ),
            Facet(
                name="size",
                type=FacetType.COUNT,
                values=["sm", "md"],
            ),
        ]

        # When
        result = client.more_like_these_search(
            more_like_these=these,
            collection_id=collection_id,
            facets=facets,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 200
        assert len(result.results) == 3
        assert len(result.facets) == len(facets)

    # endregion
