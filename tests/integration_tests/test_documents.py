#!/usr/bin/env bash

from typing import Callable

from vantage_sdk.client import VantageClient
from vantage_sdk.model.collection import UserProvidedEmbeddingsCollection


"""Integration tests for search endpoints"""


class TestDocuments:
    def test_documents_upload(
        self,
        client: VantageClient,
        account_params: dict,
        random_string_generator: Callable,
        jsonl_documents_path: str,
    ):
        """
        TODO: docstring
        """
        # Given
        batch_identifier = (
            f"test_documents_upload-{random_string_generator(6)}"
        )
        collection = UserProvidedEmbeddingsCollection(
            collection_id=random_string_generator(10),
            embeddings_dimension=1536,
            collection_name=random_string_generator(10),
        )
        client.create_collection(
            account_id=account_params["id"],
            collection=collection,
        )

        # When
        client.upsert_documents_from_jsonl_file(
            collection_id=collection.collection_id,
            file_path=jsonl_documents_path,
            batch_identifier=batch_identifier,
            account_id=account_params["id"],
        )

        # Then
        # Do nothing, if exception has not been thrown, everything is fine

    def test_parquet_upload(
        self,
        client: VantageClient,
        account_params: dict,
        random_string_generator: Callable,
        parquet_file_path: str,
    ):
        """
        TODO: docstring
        """
        # Given
        collection = UserProvidedEmbeddingsCollection(
            collection_id=random_string_generator(10),
            embeddings_dimension=1536,
            collection_name=random_string_generator(10),
        )
        client.create_collection(
            account_id=account_params["id"],
            collection=collection,
        )

        # When
        result = client.upsert_documents_from_parquet_file(
            collection_id=collection.collection_id,
            file_path=parquet_file_path,
            account_id=account_params["id"],
        )

        assert result == 200
