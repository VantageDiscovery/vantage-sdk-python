#!/usr/bin/env python

import pytest

from vantage_sdk.client import VantageClient
from vantage_sdk.core.http.exceptions import (
    BadRequestException,
    UnauthorizedException,
)
from vantage_sdk.model.search import (
    Facet,
    FacetRange,
    FacetType,
    Filter,
    MoreLikeTheseItem,
    TotalCountsOptions,
    VantageVibeImageBase64,
    VantageVibeImageUrl,
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
        search_embedding = [1.0, 1.0, 1.0, 1.0, 1.0]

        # When
        result = client.embedding_search(
            embedding=search_embedding,
            collection_id=collection_id,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 200
        assert len(result.results) == 10

    def test_embedding_search_with_partial_result(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if embedding search will return partial result.
        """
        # Given
        collection_id = test_collection_id
        search_embedding = [0.8, 0.9, 1.0, 1.0, 1.0]

        # When
        result = client.embedding_search(
            embedding=search_embedding,
            collection_id=collection_id,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 206
        assert len(result.results) == 4

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
        search_embedding = [1.0, 1.0, 1.0, 1.0, 1.0]

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
        search_embedding = [1.0, 1.0, 1.0, 1.0, 1.0]
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

    def test_semantic_search_with_partial_result(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if semantic search will return partial result.
        """
        # Given
        collection_id = test_collection_id
        accuracy = 0.2
        search_text = "partial results please"

        # When
        result = client.semantic_search(
            text=search_text,
            collection_id=collection_id,
            accuracy=accuracy,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 206
        assert len(result.results) == 4

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

    def test_more_like_this_search_returns_partial_result(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ) -> None:
        """
        Tests if MoreLikeThis search will return partial result.
        """
        # Given
        collection_id = test_collection_id
        expected_results = {"en_0370917": {"score": 0.907}}

        # When
        response = client.more_like_this_search(
            collection_id=collection_id,
            document_id="en_0530927",
            account_id=account_params["id"],
        )

        # Then
        assert response is not None
        assert response.status == 206
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

    def test_more_like_these_search_returns_partial_result(
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
                weight=0.8,
                query_text="some text",
            ),
            MoreLikeTheseItem(
                weight=0.9,
                query_text="other text",
            ),
        ]
        expected_results = {
            "en_0022659": {"score": 0.891},
            "en_0375881": {"score": 0.891},
            "en_0266579": {"score": 0.891},
        }

        response = client.more_like_these_search(
            collection_id=collection_id,
            account_id=account_params["id"],
            more_like_these=more_like_these,
        )

        # Then
        assert response is not None
        assert response.status == 206
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
        embedding = [1.0, 1.0, 1.0, 1.0, 1.0]

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

    def test_semantic_search_with_count_facets(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if semantic search will return correct result with count facets.
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

    def test_semantic_search_with_range_facets(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if semantic search will return correct result with range facets.
        """
        # Given
        collection_id = test_collection_id
        search_text = "Test search"

        facets = [
            Facet(
                name="price",
                type=FacetType.RANGE,
                ranges=[
                    FacetRange(min=0, max=99, value="below_100"),
                    FacetRange(min=100, max=1000, value="more_than_100"),
                ],
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

    def test_semantic_search_with_combined_facets(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if semantic search will return correct result with combined facets.
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
            Facet(
                name="price",
                type=FacetType.RANGE,
                ranges=[
                    FacetRange(min=0, max=99, value="below_100"),
                    FacetRange(min=100, max=1000, value="more_than_100"),
                ],
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
        embedding = [1.0, 1.0, 1.0, 1.0, 1.0]

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

    # region Additional

    def test_vantage_vibe_search(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if Vantage Vibe search will return correct result.
        """
        # Given
        collection_id = test_collection_id
        vibe_id = "test-vibe-id"
        test_images = [
            VantageVibeImageUrl(url="https://www.someimageurl.com"),
            VantageVibeImageBase64(base64="imagebase64"),
        ]
        test_text = "test search"

        # When
        response = client.vantage_vibe_search(
            vibe_id=vibe_id,
            collection_id=collection_id,
            images=test_images,
            text=test_text,
            account_id=account_params["id"],
        )

        # Then
        assert response is not None
        assert response.status == 200
        assert len(response.results) == 3

    def test_vantage_vibe_search_returns_partial_result(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if Vantage Vibe search will return correct result.
        """
        # Given
        collection_id = test_collection_id
        vibe_id = "test-vibe-id"
        test_images = [
            VantageVibeImageUrl(url="https://www.someimageurl.com"),
            VantageVibeImageBase64(base64="imagebase64"),
        ]
        test_text = "test search partial"

        # When
        response = client.vantage_vibe_search(
            vibe_id=vibe_id,
            collection_id=collection_id,
            images=test_images,
            text=test_text,
            account_id=account_params["id"],
        )

        # Then
        assert response is not None
        assert response.status == 206
        assert len(response.results) == 1

    # endregion

    # region Approximate Results Count

    def test_if_approximate_results_count_returns_result(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if approximate results count search will return correct result.
        """
        # Given
        collection_id = test_collection_id
        accuracy = 0.2
        search_text = "short legs and long body"
        total_counts = TotalCountsOptions(
            min_score_threshold=0.2, max_score_threshold=0.7
        )

        # When
        result = client.approximate_results_count_search(
            text=search_text,
            collection_id=collection_id,
            accuracy=accuracy,
            account_id=account_params["id"],
            total_counts=total_counts,
        )

        # Then
        assert result.total_count == 3

    def test_if_approximate_results_count_returns_partial_result(
        self,
        client: VantageClient,
        account_params: dict,
        test_collection_id: str,
    ):
        """
        Tests if approximate results count search will return correct result.
        """
        # Given
        collection_id = test_collection_id
        accuracy = 0.2
        search_text = "partial test"
        total_counts = TotalCountsOptions(
            min_score_threshold=0.2, max_score_threshold=0.7
        )

        # When
        result = client.approximate_results_count_search(
            text=search_text,
            collection_id=collection_id,
            accuracy=accuracy,
            account_id=account_params["id"],
            total_counts=total_counts,
        )

        # Then
        assert result.total_count == 1

    def test_if_semantic_search_with_score_treshold_returns_result(
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
        total_counts = TotalCountsOptions(
            min_score_threshold=0.2, max_score_threshold=0.7
        )

        # When
        result = client.semantic_search(
            text=search_text,
            collection_id=collection_id,
            accuracy=accuracy,
            account_id=account_params["id"],
            total_counts=total_counts,
        )

        # Then
        assert result.status == 200
        assert len(result.results) == 3

    # endregion
