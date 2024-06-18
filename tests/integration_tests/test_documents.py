#!/usr/bin/env bash

from typing import List

import pytest

from tests.integration_tests.utilities import create_temporary_upe_collection
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
        api_params: dict,
        account_params: dict,
        test_collection_id: str,
        vantage_upe_documents: List[UserProvidedEmbeddingsDocument],
    ):
        """
        TODO: docstring
        """
        # Given
        collection_id = test_collection_id
        collection_name = test_collection_id

        collection = UserProvidedEmbeddingsCollection(
            collection_id=collection_id,
            collection_name=collection_name,
            embeddings_dimension=3,
        )
        create_temporary_upe_collection(
            client=client,
            collection=collection,
            account_id=account_params["id"],
        )

        # When
        client.upsert_documents(
            collection_id=collection_id,
            documents=vantage_upe_documents,
            account_id=account_params["id"],
        )

        # Then
        # Do nothing, if exception has not been thrown, everything is fine

    def test_user_provided_documents_upsert_invalid_document_type(
        self,
        client: VantageClient,
        api_params: dict,
        account_params: dict,
        test_collection_id: str,
        vantage_vme_documents: List[VantageManagedEmbeddingsDocument],
    ):
        # Given
        collection_id = test_collection_id
        collection_name = test_collection_id

        collection = UserProvidedEmbeddingsCollection(
            collection_id=collection_id,
            collection_name=collection_name,
            embeddings_dimension=3,
        )
        create_temporary_upe_collection(
            client=client,
            collection=collection,
            account_id=account_params["id"],
        )

        # When
        with pytest.raises(ValueError) as exception:
            client.upsert_documents(
                collection_id=collection_id,
                documents=vantage_vme_documents,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is ValueError

    def test_documents_upsert_from_jsonl_file(
        self,
        client: VantageClient,
        api_params: dict,
        account_params: dict,
        test_collection_id: str,
        jsonl_documents_path: str,
    ):
        """
        TODO: docstring
        """
        # Given
        collection_id = test_collection_id
        collection_name = test_collection_id

        collection = UserProvidedEmbeddingsCollection(
            collection_id=collection_id,
            collection_name=collection_name,
            embeddings_dimension=3,
        )
        create_temporary_upe_collection(
            client=client,
            collection=collection,
            account_id=account_params["id"],
        )

        # When
        client.upsert_documents_from_jsonl_file(
            collection_id=collection_id,
            jsonl_file_path=jsonl_documents_path,
            account_id=account_params["id"],
        )

        # Then
        # Do nothing, if exception has not been thrown, everything is fine

    def test_documents_upload_from_parquet_file(
        self,
        client: VantageClient,
        account_params: dict,
        api_params: dict,
        test_collection_id: str,
        parquet_file_path: str,
    ):
        """
        TODO: docstring
        """
        # Given
        collection_id = test_collection_id
        collection_name = test_collection_id

        collection = UserProvidedEmbeddingsCollection(
            collection_id=collection_id,
            collection_name=collection_name,
            embeddings_dimension=3,
        )
        create_temporary_upe_collection(
            client=client,
            collection=collection,
            account_id=account_params["id"],
        )

        # When
        result = client.upload_documents_from_parquet_file(
            collection_id=collection_id,
            parquet_file_path=parquet_file_path,
            account_id=account_params["id"],
        )

        assert result == 200

    def test_documents_upload_from_jsonl_file(
        self,
        client: VantageClient,
        account_params: dict,
        api_params: dict,
        test_collection_id: str,
        jsonl_documents_path: str,
    ):
        """
        TODO: docstring
        """
        # Given
        collection_id = test_collection_id
        collection_name = test_collection_id

        collection = UserProvidedEmbeddingsCollection(
            collection_id=collection_id,
            collection_name=collection_name,
            embeddings_dimension=3,
        )
        create_temporary_upe_collection(
            client=client,
            collection=collection,
            account_id=account_params["id"],
        )

        # When
        result = client.upload_documents_from_jsonl_file(
            collection_id=collection_id,
            jsonl_file_path=jsonl_documents_path,
            account_id=account_params["id"],
        )

        assert result == 200
