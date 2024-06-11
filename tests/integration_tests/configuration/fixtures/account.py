import os

import pytest

from tests.integration_tests.configuration.loader import CONFIGURATION
from tests.integration_tests.configuration.mock_api import (
    get_request_stub_file_contents,
)
from tests.integration_tests.conftest import random_string


use_mock_api = CONFIGURATION["other"]["is_mock_api"]


@pytest.fixture
def updated_test_account_name(request) -> str:
    if not use_mock_api:
        return random_string(10)

    stub = get_request_stub_file_contents(request)
    return stub["response"]["jsonBody"]["account_name"]


@pytest.fixture
def non_existing_account_id(request) -> str:
    if not use_mock_api:
        return random_string(10)

    stub = get_request_stub_file_contents(request)

    return os.path.basename(stub["request"]["urlPath"])


@pytest.fixture(scope="module")
def account_params() -> dict:
    return CONFIGURATION["account"]
