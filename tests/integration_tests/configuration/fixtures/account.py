import os

import pytest

from tests.integration_tests.configuration.mock_api import (
    get_request_stub_file_contents,
)
from tests.integration_tests.conftest import random_string


use_mock_api = True if os.getenv("USE_MOCK_API", "false") == "true" else False


@pytest.fixture(scope="function")
def mock_api(request) -> None:
    if not use_mock_api:
        return
    testname = request.node.name
    assert testname == 'test_name1'


@pytest.fixture
def non_existing_user_id(request) -> str:
    if not use_mock_api:
        return random_string(10)

    testname = request.node.name
    assert testname == 'xyz'


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
