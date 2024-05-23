#!/usr/bin/env bash

from typing import Callable, List

import pytest

from vantage_sdk.client import VantageClient
from vantage_sdk.model.collection import UserProvidedEmbeddingsCollection
from vantage_sdk.model.document import (
    UserProvidedEmbeddingsDocument,
    VantageManagedEmbeddingsDocument,
)


"""Integration tests for document upsert endpoints"""


class TestDocuments:
    def test_user_provided_documents_upsert(
        self,
        client: VantageClient,
        account_params: dict,
        random_string_generator: Callable,
        vantage_upe_documents: List[UserProvidedEmbeddingsDocument],
    ):
        """
        TODO: docstring
        """
        # Given
        collection = UserProvidedEmbeddingsCollection(
            collection_id=random_string_generator(10),
            embeddings_dimension=3,
            collection_name=random_string_generator(10),
        )
        client.create_collection(
            account_id=account_params["id"],
            collection=collection,
        )

        # When
        client.upsert_documents(
            collection_id=collection.collection_id,
            documents=vantage_upe_documents,
            account_id=account_params["id"],
        )

        # Then
        # Do nothing, if exception has not been thrown, everything is fine

    def test_user_provided_documents_upsert_invalid_document_type(
        self,
        client: VantageClient,
        account_params: dict,
        random_string_generator: Callable,
        vantage_vme_documents: List[VantageManagedEmbeddingsDocument],
    ):
        # Given
        collection = UserProvidedEmbeddingsCollection(
            collection_id=random_string_generator(10),
            embeddings_dimension=3,
            collection_name=random_string_generator(10),
        )
        client.create_collection(
            account_id=account_params["id"],
            collection=collection,
        )

        # When
        with pytest.raises(ValueError) as exception:
            client.upsert_documents(
                collection_id=collection.collection_id,
                documents=vantage_vme_documents,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is ValueError

    def test_documents_upsert_from_jsonl_file(
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
            jsonl_file_path=jsonl_documents_path,
            batch_identifier=batch_identifier,
            account_id=account_params["id"],
        )

        # Then
        # Do nothing, if exception has not been thrown, everything is fine

    def test_documents_upsert_from_parquet_file(
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
            parquet_file_path=parquet_file_path,
            account_id=account_params["id"],
        )

        assert result == 200
