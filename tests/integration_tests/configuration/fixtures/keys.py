import pytest

from tests.integration_tests.configuration.loader import CONFIGURATION


@pytest.fixture(scope="module")
def vantage_api_key() -> dict:
    vantage_api_key = CONFIGURATION["keys"].get("vantage_api_key")
    if vantage_api_key is None:
        pytest.skip("No Vantage API key available.")

    return vantage_api_key


@pytest.fixture(scope="module")
def vantage_api_key_id() -> dict:
    vantage_api_key_id = CONFIGURATION["keys"].get("vantage_api_key_id")
    if vantage_api_key_id is None:
        pytest.skip("No Vantage API key ID available.")

    return vantage_api_key_id


@pytest.fixture(scope="module")
def open_api_key() -> str:
    open_api_key = CONFIGURATION["keys"].get("open_api_key")
    if open_api_key is None:
        pytest.skip("No OpenAPI key available.")

    return open_api_key


@pytest.fixture(scope="module")
def external_api_key() -> str:
    external_api_key = CONFIGURATION["keys"].get("external_api_key")
    if external_api_key is None:
        pytest.skip("No external API key available.")

    return external_api_key


@pytest.fixture(scope="module")
def external_api_key_id() -> str:
    external_api_key_id = CONFIGURATION["keys"].get("external_api_key_id")
    if external_api_key_id is None:
        pytest.skip("No external API key ID available.")

    return external_api_key_id


@pytest.fixture(scope="module")
def external_api_key_provider() -> str:
    external_api_key_provider = CONFIGURATION["keys"][
        "external_api_key_provider"
    ]
    if external_api_key_provider is None:
        pytest.skip("No external API key provider available.")

    return external_api_key_provider
