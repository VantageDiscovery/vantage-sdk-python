import pytest

from tests.integration_tests.configuration.loader import CONFIGURATION


@pytest.fixture(scope="module")
def collection_params() -> dict:
    return CONFIGURATION["collection"]
