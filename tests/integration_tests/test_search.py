#!/usr/bin/env python

from typing import Callable

import pytest

from vantage.exceptions import VantageInvalidRequestError, VantageNotFoundError
from vantage.model.search import MoreLikeTheseItem
from vantage.vantage import VantageClient


"""Integration tests for search endpoints"""


class TestSearch:
    def test_if_embedding_search_returns_result(
        self,
        client: VantageClient,
        account_params: dict,
        vantage_api_key: str,
        embedding_search_test_collection_id: str,
    ):
        """
        Tests if embedding search will return correct result.
        """
        # Given
        collection_id = embedding_search_test_collection_id
        search_embedding = [1 for col in range(1536)]
        accuracy = 0.5

        # When
        result = client.embedding_search(
            embedding=search_embedding,
            collection_id=collection_id,
            accuracy=accuracy,
            vantage_api_key=vantage_api_key,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 200
        assert result.message == "Success."
        assert len(result.results) == 10

    def test_embedding_search_on_non_existing_collection(
        self,
        client: VantageClient,
        account_params: dict,
        vantage_api_key: str,
        random_string_generator: Callable,
    ):
        """
        Tests if searching a non-existing collection will raise an exception.
        """
        # Given
        collection_id = random_string_generator(10)
        search_embedding = [1 for col in range(1536)]
        accuracy = 0.5

        # When
        with pytest.raises(VantageNotFoundError) as exception:
            client.embedding_search(
                embedding=search_embedding,
                collection_id=collection_id,
                accuracy=accuracy,
                vantage_api_key=vantage_api_key,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is VantageNotFoundError

    def test_embedding_search_with_invalid_embedding(
        self,
        client: VantageClient,
        account_params: dict,
        vantage_api_key: str,
        embedding_search_test_collection_id: str,
    ):
        """
        Tests if searching using an empty embedding will raise an exception.
        """
        # Given
        collection_id = embedding_search_test_collection_id
        search_embedding = []
        accuracy = 0.5

        # When
        with pytest.raises(VantageInvalidRequestError) as exception:
            client.embedding_search(
                embedding=search_embedding,
                collection_id=collection_id,
                accuracy=accuracy,
                vantage_api_key=vantage_api_key,
                account_id=account_params["id"],
            )
        search_embedding = [1 for col in range(1536)]
        # Then
        assert exception.type is VantageInvalidRequestError

    def test_embedding_search_with_invalid_accuracy(
        self,
        client: VantageClient,
        account_params: dict,
        vantage_api_key: str,
        embedding_search_test_collection_id: str,
    ):
        """
        Tests if searching using invalid accuracy parameter
        will raise an exception.
        """
        # Given
        collection_id = embedding_search_test_collection_id
        search_embedding = [1 for col in range(1536)]
        accuracy = 800

        # When
        with pytest.raises(VantageInvalidRequestError) as exception:
            client.embedding_search(
                embedding=search_embedding,
                collection_id=collection_id,
                accuracy=accuracy,
                vantage_api_key=vantage_api_key,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is VantageInvalidRequestError

    def test_if_semantic_search_returns_result(
        self,
        client: VantageClient,
        account_params: dict,
        vantage_api_key: str,
        semantic_search_test_collection_id: str,
    ):
        """
        Tests if semantic search will return correct result.
        """
        # Given
        collection_id = semantic_search_test_collection_id
        accuracy = 0.5
        search_text = "Test search"

        # When
        result = client.semantic_search(
            text=search_text,
            collection_id=collection_id,
            accuracy=accuracy,
            vantage_api_key=vantage_api_key,
            account_id=account_params["id"],
        )

        # Then
        assert result.status == 200
        assert result.message == "Success."
        assert len(result.results) == 10

    def test_semantic_search_on_non_existing_collection(
        self,
        client: VantageClient,
        account_params: dict,
        vantage_api_key: str,
        random_string_generator: Callable,
    ):
        """
        Tests if performing a semantic search on an non-existing collection
        will raise an exception.
        """
        # Given
        collection_id = random_string_generator(10)
        search_text = "Test search"
        accuracy = 0.5

        # When
        with pytest.raises(VantageNotFoundError) as exception:
            client.semantic_search(
                text=search_text,
                collection_id=collection_id,
                accuracy=accuracy,
                vantage_api_key=vantage_api_key,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is VantageNotFoundError

    def test_semantic_search_with_invalid_accuracy(
        self,
        client: VantageClient,
        account_params: dict,
        vantage_api_key: str,
        embedding_search_test_collection_id: str,
    ):
        """
        Tests if performing a semantic search with an invalid
        accuracy parameter will raise an exception.
        """

        # Given
        collection_id = embedding_search_test_collection_id
        search_text = "Test search"
        accuracy = 800

        # When
        with pytest.raises(VantageInvalidRequestError) as exception:
            client.semantic_search(
                text=search_text,
                collection_id=collection_id,
                accuracy=accuracy,
                vantage_api_key=vantage_api_key,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is VantageInvalidRequestError

    def test_more_like_this_search(
        self,
        client: VantageClient,
        account_params: dict,
        vantage_api_key: str,
        more_like_this_test_collection_id: str,
    ) -> None:
        """
        TODO: docstring
        """
        # Given
        expected_results = {
            "en_0982760": {"score": 0.8988204002380371},
            'en_0581405': {"score": 0.8959484100341797},
            'en_0970727': {"score": 0.8955060839653015},
        }

        # When
        response = client.more_like_this_search(
            collection_id=more_like_this_test_collection_id,
            accuracy=0.3,
            document_id="en_0340173",
            page=1,
            page_count=3,
            request_id=1,
            boolean_filter="rock",
            account_id=account_params["id"],
            vantage_api_key=vantage_api_key,
        )

        # Then
        assert response is not None
        assert response.status == 200
        assert response.message == "Success."
        results = response.results
        assert len(results) == len(expected_results)
        for result in results:
            assert result.id in expected_results.keys()
            assert expected_results[result.id]["score"] == result.score

    def test_more_like_these_search(
        self,
        client: VantageClient,
        account_params: dict,
        vantage_api_key: str,
        more_like_this_test_collection_id: str,
    ) -> None:
        """
        TODO: docstring
        """
        # Given
        more_like_these = [
            MoreLikeTheseItem(
                weight=1.0,
                query_text="bla",
            ),
            MoreLikeTheseItem(
                weight=1.0,
                query_text="bla bla",
            ),
        ]
        expected_results = {
            "en_0022659": {"score": 0.8912180066108704},
            "en_0375881": {"score": 0.891213059425354},
            "en_0266579": {"score": 0.8911941647529602},
            "en_0218966": {"score": 0.8909063339233398},
        }

        response = client.more_like_these_search(
            collection_id=more_like_this_test_collection_id,
            accuracy=0.3,
            page=1,
            page_count=5,
            request_id=1,
            boolean_filter="rock",
            account_id=account_params["id"],
            vantage_api_key=vantage_api_key,
            more_like_these=more_like_these,
        )

        # Then
        assert response is not None
        assert response.status == 200
        assert response.message == "Success."
        results = response.results
        assert len(results) == len(expected_results)
        for result in results:
            assert result.id in expected_results.keys()
            assert expected_results[result.id]["score"] == result.score
