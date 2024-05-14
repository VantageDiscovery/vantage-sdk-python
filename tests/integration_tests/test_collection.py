#!/usr/bin/env python

import time
from pathlib import Path
from typing import Callable

import pytest

from vantage_sdk.client import VantageClient
from vantage_sdk.core.exceptions import VantageFileUploadError
from vantage_sdk.core.http.exceptions import NotFoundException


class TestCollections:
    """Integration tests for collection endpoints."""

    def test_create_collection_with_user_embeddings(
        self,
        client: VantageClient,
        account_params: dict,
        collection_params: dict,
        random_string_generator: Callable,
    ) -> None:
        """
        Tests creating an empty collection with user embeddings in given account.
        """
        # Given
        collection_id = random_string_generator(10)
        collection_name = random_string_generator(10)

        # When
        collection = client.create_collection(
            account_id=account_params["id"],
            collection_id=collection_id,
            collection_name=collection_name,
            user_provided_embeddings=True,
            embeddings_dimension=1536,
        )

        # Then
        assert collection.collection_id == collection_id
        assert collection.collection_name == collection_name
        assert collection.collection_status == "Pending"
        assert collection.collection_state == "Active"

    def test_upload_user_embeddings_to_a_collection(
        self,
        client: VantageClient,
        account_params: dict,
        collection_params: dict,
        random_string_generator: Callable,
        test_parquet_file_path: str,
    ) -> None:
        """
        Tests uploading user embeddings to a collection.
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
        status = client.upsert_documents_from_parquet_file(
            collection_id=collection_id,
            parquet_file_path=test_parquet_file_path,
            account_id=account_params["id"],
        )

        # Then
        assert status == 200

    def test_upload_user_embeddings_to_a_non_existing_collection(
        self,
        client: VantageClient,
        account_params: dict,
        collection_params: dict,
        random_string_generator: Callable,
        test_parquet_file_path: str,
    ) -> None:
        """
        Tests uploading user embeddings to a non-existing collection.
        """
        # Given
        collection_id = random_string_generator(10)

        with pytest.raises(NotFoundException) as exception:
            client.upsert_documents_from_parquet_file(
                collection_id=collection_id,
                parquet_file_path=test_parquet_file_path,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is NotFoundException

    def test_upload_non_existing_user_embeddings(
        self,
        client: VantageClient,
        account_params: dict,
        collection_params: dict,
        random_string_generator: Callable,
        test_parquet_file_path: str,
    ) -> None:
        """
        Tests uploading non existing user embeddings file.
        """
        # Given
        collection_id = random_string_generator(10)
        non_existing_file_path = random_string_generator(10)

        with pytest.raises(FileNotFoundError) as exception:
            client.upsert_documents_from_parquet_file(
                collection_id=collection_id,
                parquet_file_path=non_existing_file_path,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is FileNotFoundError

    def test_upload_user_embeddings_with_wrong_file_size(
        self,
        client: VantageClient,
        account_params: dict,
        collection_params: dict,
        random_string_generator: Callable,
        test_parquet_file_path: str,
    ):
        """
        Tests uploading user embeddings with wrong file size specified.
        """
        # Given
        file_size = Path(test_parquet_file_path).stat().st_size + 1
        file = open(test_parquet_file_path, "rb")
        file_content = file.read()
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
        with pytest.raises(VantageFileUploadError) as exception:
            client._upsert_documents_from_bytes(
                collection_id=collection_id,
                content=file_content,
                file_size=file_size,
                batch_identifier="test-batch",
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is VantageFileUploadError
        assert exception.value.args == ("Forbidden", 403)

    def test_create_vantage_managed_embeddings_collection(
        self,
        client: VantageClient,
        account_params: dict,
        collection_params: dict,
        random_string_generator: Callable,
    ) -> None:
        """
        Tests creating an empty collection with vantage managed
        embeddings in given account.
        """
        # TODO: Needs external model API key
        ...

    def test_list_collections(
        self,
        client: VantageClient,
        random_string_generator: Callable,
        account_params: dict,
    ) -> None:
        """
        Tests listing collections.
        This test will first create a number of collections,
        and then test if created collections are among listed collections.
        """
        # Given
        collections_count = 5
        collection_names = [
            random_string_generator(10) for _ in range(collections_count)
        ]
        for collection_name in collection_names:
            client.create_collection(
                account_id=account_params["id"],
                collection_id=collection_name,
                collection_name=collection_name,
                user_provided_embeddings=True,
                embeddings_dimension=1536,
            )

        # When
        collections = client.list_collections()

        # Then
        created_collections = list(
            filter(
                lambda collection: collection.collection_name
                in collection_names,
                collections,
            )
        )
        assert len(created_collections) == collections_count
        for collection in created_collections:
            assert collection.collection_name == collection.collection_id
            assert collection.collection_id in collection_names
            assert collection.collection_name in collection_names

    def test_get_collection(
        self,
        client: VantageClient,
        account_params: dict,
        random_string_generator: Callable,
    ) -> None:
        """
        Tests if it can retrieve a single collection.
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
        collection = client.get_collection(
            collection_id=collection_id, account_id=account_params["id"]
        )

        # Then
        assert collection.collection_id == collection_id
        assert collection.collection_name == collection_name
        assert collection.collection_status == "Pending"
        assert collection.collection_state is None

    def test_get_non_existing_collection(
        self,
        client: VantageClient,
        account_params: dict,
        random_string_generator: Callable,
    ) -> None:
        """
        Tests if fetching a non-existing collection will raise an exception.
        """
        # Given
        collection_id = random_string_generator(10)

        # When
        with pytest.raises(NotFoundException) as exception:
            client.get_collection(
                collection_id=collection_id, account_id=account_params["id"]
            )

        # Then
        assert exception.type is NotFoundException

    def test_update_collection(
        self,
        client: VantageClient,
        account_params: dict,
        random_string_generator: Callable,
    ) -> None:
        """
        Tests if an existing collection can be updated.
        """
        # Given
        collection_id = random_string_generator(10)
        collection_name = collection_id
        client.create_collection(
            account_id=account_params["id"],
            collection_id=collection_id,
            collection_name=collection_name,
            user_provided_embeddings=True,
            embeddings_dimension=1536,
        )
        updated_collection_name = random_string_generator(10)
        updated_url_pattern = random_string_generator(10)
        # Take a nap while API sets up a collection.
        time.sleep(3)

        # When
        collection = client.update_collection(
            collection_id=collection_id,
            account_id=account_params["id"],
            collection_name=updated_collection_name,
            collection_preview_url_pattern=updated_url_pattern,
        )

        # Then
        assert collection.collection_name == updated_collection_name
        assert collection.collection_preview_url_pattern == updated_url_pattern

    def test_update_non_existing_collection(
        self,
        client: VantageClient,
        account_params: dict,
        random_string_generator: Callable,
    ) -> None:
        """
        Tests if updating a non-existing collection will raise an exception.
        """
        # When
        with pytest.raises(NotFoundException) as exception:
            client.update_collection(
                collection_id=random_string_generator(10),
                account_id=account_params["id"],
                collection_name=random_string_generator(10),
                external_key_id=random_string_generator(10),
                collection_preview_url_pattern=random_string_generator(10),
            )

        # Then
        assert exception.type is NotFoundException

    def test_delete_collection(
        self,
        client: VantageClient,
        account_params: dict,
        collection_params: dict,
        random_string_generator: Callable,
    ) -> None:
        """
        Tests if an existing collection can be deleted.
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
        client.delete_collection(
            collection_id=collection_id, account_id=account_params["id"]
        )

        # Then
        with pytest.raises(NotFoundException) as exception:
            client.get_collection(
                collection_id=collection_id, account_id=account_params["id"]
            )
        assert exception.type is NotFoundException

        listed_deleted_collection = list(
            filter(
                lambda col: col.collection_id == collection_id,
                client.list_collections(),
            )
        )
        assert len(listed_deleted_collection) == 0

    def test_delete_non_existing_collection(
        self,
        client: VantageClient,
        account_params: dict,
        random_string_generator: Callable,
    ) -> None:
        """
        Tests if deleting a non-existing collection will raise an exception.
        """
        # Given
        collection_id = random_string_generator(10)

        # When
        with pytest.raises(NotFoundException) as exception:
            client.delete_collection(
                collection_id=collection_id, account_id=account_params["id"]
            )

        # Then
        assert exception.type is NotFoundException
