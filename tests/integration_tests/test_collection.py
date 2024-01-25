#!/usr/bin/env python

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
    Tests creating an empty collection in given user account.
    Collection ID and name are generated randomly.
    """

    def test_create_collection(
        self,
        client: Vantage,
        account_params: dict,
        collection_params: dict,
        random_string: str,
    ) -> None:
        # Given
        collection_id = random_string
        collection_name = random_string

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
    TODO: documentation.
    """

    def test_list_collections(self, client: Vantage) -> None:
        # TODO: implement
        ...

    """
    TODO: documentation.
    """

    def test_get_collection(self, client: Vantage) -> None:
        # TODO: implement
        ...

    """
    TODO: documentation.
    """

    def test_update_collection(self, client: Vantage) -> None:
        # TODO: implement
        ...

    """
    TODO: documentation.
    """

    def test_delete_collection(self, client: Vantage) -> None:
        # TODO: implement
        ...
