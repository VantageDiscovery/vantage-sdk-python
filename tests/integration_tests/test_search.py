#!/usr/bin/env python

from typing import Callable

import pytest

from vantage.core.http.exceptions import BadRequestException
from vantage.exceptions import VantageNotFoundException
from vantage.model import MoreLikeThese
from vantage.vantage import Vantage


"""Integration tests for search endpoints"""


class TestSearch:
    def test_if_embedding_search_returns_result(
        self,
        client: Vantage,
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
        client: Vantage,
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
        with pytest.raises(VantageNotFoundException) as exception:
            client.embedding_search(
                embedding=search_embedding,
                collection_id=collection_id,
                accuracy=accuracy,
                vantage_api_key=vantage_api_key,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is VantageNotFoundException

    def test_embedding_search_with_invalid_embedding(
        self,
        client: Vantage,
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
        with pytest.raises(BadRequestException) as exception:
            client.embedding_search(
                embedding=search_embedding,
                collection_id=collection_id,
                accuracy=accuracy,
                vantage_api_key=vantage_api_key,
                account_id=account_params["id"],
            )
        search_embedding = [1 for col in range(1536)]
        # Then
        assert exception.type is BadRequestException

    def test_embedding_search_with_invalid_accuracy(
        self,
        client: Vantage,
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
        with pytest.raises(BadRequestException) as exception:
            client.embedding_search(
                embedding=search_embedding,
                collection_id=collection_id,
                accuracy=accuracy,
                vantage_api_key=vantage_api_key,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is BadRequestException

    def test_if_semantic_search_returns_result(
        self,
        client: Vantage,
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
        client: Vantage,
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
        with pytest.raises(VantageNotFoundException) as exception:
            client.semantic_search(
                text=search_text,
                collection_id=collection_id,
                accuracy=accuracy,
                vantage_api_key=vantage_api_key,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is VantageNotFoundException

    def test_semantic_search_with_invalid_accuracy(
        self,
        client: Vantage,
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
        with pytest.raises(BadRequestException) as exception:
            client.semantic_search(
                text=search_text,
                collection_id=collection_id,
                accuracy=accuracy,
                vantage_api_key=vantage_api_key,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is BadRequestException

    def test_more_like_this_search(
        self,
        client: Vantage,
        account_params: dict,
        vantage_api_key: str,
        more_like_this_test_collection_id: str,
    ) -> None:
        result = client.more_like_this_search(
            collection_id=more_like_this_test_collection_id,
            accuracy=0.5,
            document_id="00",
            page=1,
            page_count=5,
            request_id=1,
            boolean_filter="bread",
            account_id=account_params["id"],
            vantage_api_key=vantage_api_key,
        )

        assert result is not None

    def test_more_like_these_search(
        self,
        client: Vantage,
        account_params: dict,
        vantage_api_key: str,
        more_like_this_test_collection_id: str,
    ) -> None:
        more_like_these = [
            MoreLikeThese(
                weight=0.5,
                query_text="asdlkj",
                query_document_id="asdklj",
                embedding=[1, 2],
                these=[{"yes": "nope"}],
            )
        ]

        result = client.more_like_these_search(
            collection_id=more_like_this_test_collection_id,
            accuracy=0.5,
            page=1,
            page_count=5,
            request_id=1,
            boolean_filter="hello",
            account_id=account_params["id"],
            vantage_api_key=vantage_api_key,
            more_like_these=more_like_these,
        )

        assert result is not None
