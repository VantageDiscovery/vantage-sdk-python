from typing import Callable

import pytest

from vantage.core.http.exceptions import ForbiddenException, ServiceException
from vantage.vantage import Vantage


"""Integration tests for API keys endpoints."""


class TestApiKeys:
    pass

    def test_get_vantage_api_keys(self, client: Vantage, account_params: dict):
        # When
        keys = client.get_vantage_api_keys(account_id=account_params["id"])

        # Then
        assert len(keys) == 1
        api_key = keys[0]
        assert api_key.actual_instance.vantage_api_key_value is None
        assert api_key.actual_instance.account_id == account_params["id"]

    def test_get_vantage_api_keys_using_wrong_account(
        self,
        client: Vantage,
        random_string_generator: Callable,
    ):
        # When
        with pytest.raises(ForbiddenException) as exception:
            client.get_vantage_api_keys(account_id=random_string_generator(10))

        # Then
        assert exception.type == ForbiddenException

    def test_get_vantage_api_key(
        self,
        client: Vantage,
        account_params: dict,
        vantage_api_key_id: str,
    ):
        # When
        api_key = client.get_vantage_api_key(
            vantage_api_key_id=vantage_api_key_id,
            account_id=account_params["id"],
        )

        # Then
        assert api_key.account_id == account_params["id"]
        assert api_key.vantage_api_key_value is None
        api_key.vantage_api_key_id == vantage_api_key_id

    def test_get_vantage_api_key_using_wrong_account(
        self,
        client: Vantage,
        vantage_api_key_id: str,
        random_string_generator: Callable,
    ):
        # When
        with pytest.raises(ForbiddenException) as exception:
            client.get_vantage_api_key(
                vantage_api_key_id=vantage_api_key_id,
                account_id=random_string_generator(10),
            )

        # Then
        assert exception.type == ForbiddenException

    def test_get_non_existing_vantage_api_key(
        self,
        client: Vantage,
        account_params: dict,
        vantage_api_key_id: str,
        random_string_generator: Callable,
    ):
        # When
        with pytest.raises(ServiceException) as exception:
            client.get_vantage_api_key(
                vantage_api_key_id=random_string_generator(10)
            )

        # Then
        assert exception.type is ServiceException
