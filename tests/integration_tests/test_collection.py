#!/usr/bin/env python

from typing import Callable

import pytest

from vantage.exceptions import VantageNotFoundException
from vantage.vantage import Vantage


"""Integration tests for collection endpoints."""


class TestCollections:
    """
    Takes care of setting up and tearing down test conditions.
    """

    @pytest.fixture(autouse=True)
    def setup_and_teardown(
        self, client: Vantage, account_params: dict, collection_params: dict
    ) -> None:
        # Setup
        yield
        # Teardown
        try:
            collections = client.list_collections(
                account_id=account_params["id"]
            )
            for collection in collections:
                client.delete_collection(
                    collection_id=collection.actual_instance.collection_id,
                    account_id=account_params["id"],
                )
        except VantageNotFoundException:
            # Do nothing
            pass

    """
    Tests creating an empty collection with user embeddings in given account.
    """

    def test_create_collection_with_user_embeddings(
        self,
        client: Vantage,
        account_params: dict,
        collection_params: dict,
        random_string_generator: Callable,
    ) -> None:
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

    """
    Tests uploading user embeddings to a collection.
    """

    def test_upload_user_embeddings_to_a_collection(
        self,
        client: Vantage,
        account_params: dict,
        collection_params: dict,
        random_string_generator: Callable,
        test_parquet_file_path: str,
    ) -> None:
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
        status = client.upload_embedding_by_path(
            collection_id=collection_id,
            file_path=test_parquet_file_path,
            customer_batch_identifier="automated-tests",
            account_id=account_params["id"],
        )

        # Then
        assert status == 200

    """
    Tests creating an empty collection with vantage managed
    embeddings in given account.
    """

    def test_create_vantage_managed_embeddings_collection(
        self,
        client: Vantage,
        account_params: dict,
        collection_params: dict,
        random_string_generator: Callable,
    ) -> None:
        # TODO: Needs external model API key
        ...

    """
    Tests listing collections.
    This test will first create a number of collections,
    and then test if created collections are among listed collections.
    """

    def test_list_collections(
        self,
        client: Vantage,
        random_string_generator: Callable,
        account_params: dict,
    ) -> None:
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
                lambda collection: collection.actual_instance.collection_name
                in collection_names,
                collections,
            )
        )
        assert len(created_collections) == collections_count
        for collection in created_collections:
            assert (
                collection.actual_instance.collection_name
                == collection.actual_instance.collection_id
            )
            assert collection.actual_instance.collection_id in collection_names
            assert (
                collection.actual_instance.collection_name in collection_names
            )

    """
    Tests if it can retrieve a single collection.
    """

    def test_get_collection(
        self,
        client: Vantage,
        account_params: dict,
        random_string_generator: Callable,
    ) -> None:
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
        assert collection.collection_state == "Active"

    """
    Tests if fetching a non-existing collection will raise an exception.
    """

    def test_get_non_existing_collection(
        self,
        client: Vantage,
        account_params: dict,
        random_string_generator: Callable,
    ) -> None:
        # Given
        collection_id = random_string_generator(10)

        # When
        with pytest.raises(VantageNotFoundException) as exception:
            client.get_collection(
                collection_id=collection_id, account_id=account_params["id"]
            )

        # Then
        assert exception.type is VantageNotFoundException

    """
    Tests if an existing collection can be updated.
    """

    def test_update_collection(
        self,
        client: Vantage,
        account_params: dict,
        random_string_generator: Callable,
    ) -> None:
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

    """
    Tests if updating a non-existing collection will raise an exception.
    """

    def test_update_non_existing_collection(
        self,
        client: Vantage,
        account_params: dict,
        random_string_generator: Callable,
    ) -> None:
        # When
        with pytest.raises(VantageNotFoundException) as exception:
            client.update_collection(
                collection_id=random_string_generator(10),
                account_id=account_params["id"],
                collection_name=random_string_generator(10),
                external_key_id=random_string_generator(10),
                collection_preview_url_pattern=random_string_generator(10),
            )

        # Then
        assert exception.type is VantageNotFoundException

    """
    Tests if an existing collection can be deleted.
    """

    def test_delete_collection(
        self,
        client: Vantage,
        account_params: dict,
        collection_params: dict,
        random_string_generator: Callable,
    ) -> None:
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
        with pytest.raises(VantageNotFoundException) as exception:
            client.get_collection(
                collection_id=collection_id, account_id=account_params["id"]
            )
        assert exception.type is VantageNotFoundException

        listed_deleted_collection = list(
            filter(
                lambda col: col.collection_id == collection_id,
                client.list_collections(),
            )
        )
        assert len(listed_deleted_collection) == 0

    """
    Tests if deleting a non-existing collection will raise an exception.
    """

    def test_delete_non_existing_collection(
        self,
        client: Vantage,
        account_params: dict,
        random_string_generator: Callable,
    ) -> None:
        # Given
        collection_id = random_string_generator(10)

        # When
        with pytest.raises(VantageNotFoundException) as exception:
            client.delete_collection(
                collection_id=collection_id, account_id=account_params["id"]
            )

        # Then
        assert exception.type is VantageNotFoundException
