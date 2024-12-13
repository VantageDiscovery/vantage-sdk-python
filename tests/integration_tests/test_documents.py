#!/usr/bin/env bash

from typing import List

import pytest
from pydantic import ValidationError

from tests.integration_tests.utilities import create_temporary_upe_collection
from vantage_sdk.client import VantageClient
from vantage_sdk.model.collection import UserProvidedEmbeddingsCollection
from vantage_sdk.model.document import (
    GetDocumentsRequestDocument,
    MetadataItem,
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

    def test_valid_embeddings_document_creation(
        self,
    ):
        # Given
        embedding_vector = [1.0, 0.0, 0.0]

        # When
        UserProvidedEmbeddingsDocument(
            embeddings=embedding_vector,
        )

        assert 1 == 1

    def test_invalid_embeddings_document_creation(
        self,
    ):
        # Given
        embedding_vector = [1.0, 1.0, 1.0]

        # When
        with pytest.raises(ValidationError) as exception:
            UserProvidedEmbeddingsDocument(
                embeddings=embedding_vector,
            )

        # Then
        assert exception.type is ValidationError

    def test_sortable_metadata(
        self,
    ):
        # Given
        embedding_vector = [1.0]
        metadata = [
            MetadataItem(key="price", value=1.0, sortable=True),
        ]

        # When
        document = UserProvidedEmbeddingsDocument(
            embeddings=embedding_vector,
            metadata=metadata,
        )

        # Then
        assert document.metadata[0].key == "meta_ordered_price"

    def test_sortable_metadata_not_float(
        self,
    ):
        # When
        with pytest.raises(ValidationError) as exception:
            MetadataItem(key="price", value=1, sortable=True)

        # Then
        assert exception.type is ValidationError

    def test_query_documents(
        self,
        client: VantageClient,
        test_collection_id: str,
    ):
        # Given
        collection_id = test_collection_id
        fields = ["title", "description", "color"]
        ids = [
            GetDocumentsRequestDocument(
                id="product|8072876490904",
                variant_ids=[
                    "43998558322840",
                    "43998558716056",
                ],
            ),
            GetDocumentsRequestDocument(
                id="product|3122876490424",
                variant_ids=[],
            ),
        ]

        # When
        response = client.query_documents(
            collection_id=collection_id,
            fields=fields,
            ids=ids,
        )

        # Then
        assert response is not None
        assert response.status == 200
        assert response.message == "Success"
        documents = response.documents
        assert documents is not None
        assert len(documents) == 2
        first_document = documents[0]
        second_document = documents[1]

        assert first_document.id == "product|8072876490904"
        assert first_document.fields.get("title") == "Hasbro Car Toy"
        assert first_document.fields.get("description").startswith(
            "A ready-made car toy"
        )
        for variant in first_document.variants:
            assert variant.id is not None
            assert variant.fields is not None

        assert second_document.id == "product|3122876490424"
        assert second_document.fields.get("title") == "Hasbro Airplane Toy"
        assert second_document.fields.get("description").startswith(
            "A simple airplane toy"
        )
        assert len(second_document.variants) == 0
