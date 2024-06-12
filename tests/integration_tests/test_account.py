#!/usr/bin/env python
from typing import Callable

import pytest

from vantage_sdk.client import VantageClient
from vantage_sdk.core.http.exceptions import ForbiddenException


""" Integration tests for account endpoints."""


class TestAccount:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(
        self, client: VantageClient, account_params: dict
    ) -> None:
        """
        Takes care of setting up and tearing down test conditions.
        Runs before and after each test.
        """
        # Setup
        client.update_account(account_params["id"], account_params["id"])
        yield
        # Teardown
        client.update_account(account_params["id"], account_params["id"])

    def test_get_account(
        self, client: VantageClient, account_params: dict
    ) -> None:
        """
        Tests if retrieving user account is working correctly.
        """
        # Given
        test_account_id = account_params["id"]
        test_account_name = account_params["name"]

        # When
        account = client.get_account(test_account_id)

        # Then
        assert account.account_name == test_account_name

    def test_get_non_existing_account(
        self,
        client: VantageClient,
        account_params: dict,
        non_existing_account_id: str,
    ) -> None:
        """
        Tests if retrieving non-existing user account throws an exception.
        """

        # When
        with pytest.raises(ForbiddenException) as exception:
            client.get_account(non_existing_account_id)

        # Then
        assert exception.type is ForbiddenException

    def test_update_account(
        self,
        client: VantageClient,
        account_params: dict,
        updated_test_account_name,
    ) -> None:
        """
        Tests if updating user account is working correctly.
        """
        # Given
        test_account_id = account_params["id"]

        # When
        client.update_account(
            account_id=test_account_id, account_name=updated_test_account_name
        )

        # Then
        account = client.get_account(test_account_id)
        assert account.account_name == updated_test_account_name

    def test_update_non_existing_account(
        self,
        client: VantageClient,
        account_params: dict,
        non_existing_account_id: str,
        random_string_generator: Callable,
    ) -> None:
        """
        Tests if updating non-existing user account throws an exception.
        """
        # Given
        non_existing_account_id = non_existing_account_id
        non_existing_account_name = non_existing_account_id

        # When
        with pytest.raises(ForbiddenException) as exception:
            client.update_account(
                non_existing_account_id, non_existing_account_name
            )

        # Then
        assert exception.type is ForbiddenException
