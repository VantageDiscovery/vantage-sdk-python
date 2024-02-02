#!/usr/bin/env python

from typing import Callable

import pytest

from vantage.core.http.exceptions import BadRequestException
from vantage.exceptions import VantageNotFoundException
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
