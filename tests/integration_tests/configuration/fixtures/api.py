import pytest

from tests.integration_tests.configuration.loader import CONFIGURATION


@pytest.fixture(scope="module")
def api_params() -> dict:
    return CONFIGURATION["api"]


@pytest.fixture(scope="module")
def mock_api() -> dict:
    return CONFIGURATION["other"]["is_mock_api"]
