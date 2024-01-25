#!/usr/bin/env python
import pytest

from vantage.vantage import Vantage


""" Integration tests for account endpoints."""


class TestAccount:
    """
    Takes care of setting up and tearing down test conditions.
    """

    @pytest.fixture(autouse=True)
    def setup_and_teardown(
        self, client: Vantage, account_params: dict
    ) -> None:
        # Setup
        client.update_account(account_params["id"], account_params["id"])
        yield
        # Teardown
        client.update_account(account_params["id"], account_params["id"])

    """
    Tests if retrieving user account is working correctly.
    """

    def test_get_account(self, client: Vantage, account_params: dict) -> None:
        # Given
        test_account_id = account_params["id"]
        test_account_name = account_params["name"]

        # When
        account = client.get_account(test_account_id)

        # Then
        assert account.account_name == test_account_name

    """
    Tests if updating user account is working correctly.
    """

    def test_update_account(
        self, client: Vantage, account_params: dict, random_string: str
    ) -> None:
        # Given
        test_account_id = account_params["id"]
        updated_test_account_name = random_string

        # When
        client.update_account(test_account_id, updated_test_account_name)

        # Then
        account = client.get_account(test_account_id)
        assert account.account_name == updated_test_account_name
