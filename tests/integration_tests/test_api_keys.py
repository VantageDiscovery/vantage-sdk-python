from typing import Callable

import pytest

from tests.integration_tests.conftest import skip_delete_external_api_key_test
from vantage.core.http.exceptions import ForbiddenException, ServiceException
from vantage.vantage import Vantage


"""Integration tests for API keys endpoints."""


class TestApiKeys:
    def test_get_vantage_api_keys(self, client: Vantage, account_params: dict):
        """
        Tests fetching all vantage API keys present on a user account.
        """
        # When
        keys = client.get_vantage_api_keys(account_id=account_params["id"])

        # Then
        assert len(keys) == 1
        api_key = keys[0]
        assert api_key.vantage_api_key_value is None
        assert api_key.account_id == account_params["id"]

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
        """
        Tests fetching single vantage API key present on a user account.
        """
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
        """
        Tests fetching a single Vantage API key using non-existing account ID.
        """
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
        random_uuid: str,
    ):
        """
        Tests fetching a non-existing Vantage API key from a user account.
        """
        # When
        with pytest.raises(ServiceException) as exception:
            client.get_vantage_api_key(vantage_api_key_id=random_uuid)

        # Then
        assert exception.type is ServiceException

    def test_get_external_api_keys(
        self,
        client: Vantage,
        account_params: dict,
        external_api_key: str,
        external_api_key_id: str,
        external_api_key_provider: str,
    ):
        """
        Tests fetching all external API keys from a users' account.
        """
        # When
        keys = client.get_external_api_keys(account_id=account_params["id"])

        # Then
        assert len(keys) == 1
        api_key = keys[0]
        assert api_key.account_id == account_params["id"]
        assert api_key.external_key_id == external_api_key_id
        assert api_key.llm_provider == external_api_key_provider
        assert api_key.llm_secret == external_api_key

    def test_get_external_api_key(
        self,
        client: Vantage,
        account_params: dict,
        external_api_key: str,
        external_api_key_id: str,
        external_api_key_provider: str,
    ):
        """
        Tests fetching a single external API key from a users' account.
        """
        # When
        api_key = client.get_external_api_key(
            account_id=account_params["id"],
            external_key_id=external_api_key_id,
        )

        # Then
        assert api_key.account_id == account_params["id"]
        assert api_key.external_key_id == external_api_key_id
        assert api_key.llm_provider == external_api_key_provider
        assert api_key.llm_secret == external_api_key

    def test_get_non_existing_external_api_key(
        self,
        client: Vantage,
        account_params: dict,
        random_uuid: str,
    ):
        """
        Tests fetching a non-existing external API key from a users' account.
        """
        # When
        with pytest.raises(ServiceException) as exception:
            client.get_external_api_key(
                account_id=account_params["id"],
                external_key_id=random_uuid,
            )

        # Then
        assert exception.type is ServiceException

    def test_create_external_api_key(
        self,
        client: Vantage,
        account_params: dict,
        external_api_key_id: str,
        random_string_generator: str,
    ):
        """
        Tests creating an external API key on a users' account.
        """
        # Given
        url = f"http://{random_string_generator(10)}"
        llm_provider = "OpenAI"
        llm_secret = random_string_generator(10)

        # When
        response = client.create_external_api_key(
            url=url,
            llm_provider=llm_provider,
            llm_secret=llm_secret,
            account_id=account_params["id"],
        )

        # Then
        assert response is not None
        assert response.account_id == account_params["id"]
        assert response.llm_provider == llm_provider
        assert response.llm_secret == llm_secret
        assert response.url == url

        # After
        client.delete_external_api_key(
            external_key_id=response.external_key_id,
            account_id=account_params["id"],
        )

    def test_update_external_api_key(
        self,
        client: Vantage,
        account_params: dict,
        external_api_key_id: str,
        random_string_generator: str,
    ):
        """
        Tests updating an external API key present on a users' account.
        """
        # Given
        url = f"http://{random_string_generator(10)}"
        llm_provider = "Hugging"
        llm_secret = random_string_generator(10)
        api_key = client.get_external_api_key(
            external_key_id=external_api_key_id,
            account_id=account_params["id"],
        )
        given_url = api_key.url
        given_llm_provider = api_key.llm_provider
        given_llm_secret = api_key.llm_secret

        client.update_external_api_key(
            external_key_id=external_api_key_id,
            url=url,
            llm_provider=llm_provider,
            llm_secret=llm_secret,
            account_id=account_params["id"],
        )
        # When
        api_key = client.get_external_api_key(
            account_id=account_params["id"],
            external_key_id=external_api_key_id,
        )

        # Then
        assert api_key.account_id == account_params["id"]
        assert api_key.external_key_id == external_api_key_id
        assert api_key.llm_provider == llm_provider
        assert api_key.llm_secret == llm_secret
        assert api_key.url == url

        # After
        client.update_external_api_key(
            external_key_id=external_api_key_id,
            url=given_url,
            llm_provider=given_llm_provider,
            llm_secret=given_llm_secret,
            account_id=account_params["id"],
        )

    def test_update_non_existing_external_api_key(
        self,
        client: Vantage,
        account_params: dict,
        random_uuid: str,
        random_string_generator: Callable,
    ):
        """
        Tests updating a non-existing external API key
        on a users' account.
        """
        # When
        with pytest.raises(ServiceException) as exception:
            client.update_external_api_key(
                external_key_id=random_uuid,
                url=random_string_generator(10),
                llm_provider=random_string_generator(10),
                llm_secret=random_string_generator(10),
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is ServiceException

    @pytest.mark.skipif(
        skip_delete_external_api_key_test(), reason="Test disabled by user."
    )
    def test_delete_external_api_key(
        self,
        client: Vantage,
        account_params: dict,
        external_api_key_id: str,
    ):
        """
        Tests deleting an existing external API key on users' account.
        """
        # When
        api_key = client.delete_external_api_key(
            external_key_id=external_api_key_id,
            account_id=account_params["id"],
        )

        # Then
        assert api_key is None
        with pytest.raises(ServiceException) as exception:
            client.get_external_api_key(
                external_key_id=external_api_key_id,
                account_id=account_params["id"],
            )
        assert exception.type is ServiceException

    def test_delete_non_existing_external_api_key(
        self,
        client: Vantage,
        account_params: dict,
        random_uuid: str,
    ):
        """
        Tests deleting a non-existing external API key on users' account.
        """
        # When
        with pytest.raises(ServiceException) as exception:
            client.delete_external_api_key(
                external_key_id=random_uuid,
                account_id=account_params["id"],
            )

        # Then
        assert exception.type is ServiceException
