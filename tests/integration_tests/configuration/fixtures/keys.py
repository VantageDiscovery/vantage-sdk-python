import os

import pytest

from tests.integration_tests.configuration.loader import CONFIGURATION
from tests.integration_tests.configuration.mock_api import (
    get_request_stub_file_contents,
)
from tests.integration_tests.conftest import random_string


use_mock_api = CONFIGURATION["other"]["is_mock_api"]


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


@pytest.fixture(scope="function")
def external_api_key_id(request) -> str:
    if not use_mock_api:
        external_api_key_id = CONFIGURATION["keys"].get("external_api_key_id")
        if external_api_key_id is None:
            pytest.skip("No external API key ID available.")

        return external_api_key_id

    stub = get_request_stub_file_contents(request)
    return os.path.basename(stub["request"]["urlPath"])


@pytest.fixture(scope="module")
def external_api_key_provider() -> str:
    external_api_key_provider = CONFIGURATION["keys"][
        "external_api_key_provider"
    ]
    if external_api_key_provider is None:
        pytest.skip("No external API key provider available.")

    return external_api_key_provider


@pytest.fixture(scope="function")
def api_key_nonexisting_account_id(request) -> str:
    if not use_mock_api:
        return random_string(10)

    stub = get_request_stub_file_contents(request)

    return stub["request"]["urlPath"].split("/")[3]


@pytest.fixture(scope="function")
def nonexisting_api_key_id(request) -> str:
    if not use_mock_api:
        return random_string(10)

    stub = get_request_stub_file_contents(request)

    return os.path.basename(stub["request"]["urlPath"])


@pytest.fixture(scope="function")
def nonexisting_external_api_key_id(request) -> str:
    if not use_mock_api:
        return random_string(10)

    stub = get_request_stub_file_contents(request)

    return os.path.basename(stub["request"]["urlPath"])


@pytest.fixture(scope="function")
def external_key_llm_secret(request) -> str:
    if not use_mock_api:
        return random_string(10)

    stub = get_request_stub_file_contents(request)

    try:
        return os.path.basename(stub["response"]["jsonBody"]["llm_secret"])
    except KeyError:
        return CONFIGURATION["keys"]["llm_secret"]


@pytest.fixture(scope="function")
def external_key_updated_llm_secret(request) -> str:
    if not use_mock_api:
        return random_string(10)

    stub = get_request_stub_file_contents(request)

    return os.path.basename(stub["response"]["jsonBody"]["llm_secret"])
