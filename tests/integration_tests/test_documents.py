#!/usr/bin/env bash

from typing import Callable

from vantage.vantage import VantageClient


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
        collection_id = random_string_generator(10)
        collection_name = random_string_generator(10)
        batch_identifier = (
            f"test_documents_upload-{random_string_generator(6)}"
        )

        client.create_collection(
            account_id=account_params["id"],
            collection_id=collection_id,
            collection_name=collection_name,
            user_provided_embeddings=True,
            embeddings_dimension=1536,
        )

        # When
        client.upload_documents_from_path(
            collection_id=collection_id,
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
        collection_id = random_string_generator(10)
        collection_name = random_string_generator(10)

        client.create_collection(
            account_id=account_params["id"],
            collection_id=collection_id,
            collection_name=collection_name,
            user_provided_embeddings=True,
            embeddings_dimension=1536,
        )

        # When
        result = client.upload_embeddings_from_parquet(
            collection_id=collection_id,
            file_path=parquet_file_path,
            account_id=account_params["id"],
        )

        assert result == 200
