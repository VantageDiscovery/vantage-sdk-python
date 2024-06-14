import os
import random
import string
import uuid
from typing import Callable

import pytest

from tests.integration_tests.configuration.client import create_client
from tests.integration_tests.configuration.loader import CONFIGURATION
from vantage_sdk.client import VantageClient


if CONFIGURATION["other"]["is_mock_api"]:
    from tests.integration_tests.configuration.mock_api import setup_mock

    setup_mock(CONFIGURATION["api"]["api_host"])


auth_method = CONFIGURATION["auth"]["auth_method"]
jwt_token = CONFIGURATION["auth"]["jwt_token"]

_client = create_client(
    auth_method=auth_method,
    jwt_token=jwt_token,
    configuration=CONFIGURATION,
)

_protected_collections = []

embedding_collection_id = CONFIGURATION["collection"].get(
    "embedding_search_test_collection_id"
)
semantic_colection_id = CONFIGURATION["collection"].get(
    "semantic_search_test_collection_id"
)
mlt_collection_id = CONFIGURATION["collection"].get(
    "more_like_this_collection"
)
if embedding_collection_id:
    _protected_collections.append(embedding_collection_id)
if semantic_colection_id:
    _protected_collections.append(semantic_colection_id)
if mlt_collection_id:
    _protected_collections.append(mlt_collection_id)


def skip_delete_external_api_key_test() -> bool:
    """
    Used to determine if TestApiKeys::test_delete_external_api_key test
    should run.
    """
    value = os.getenv("ENABLE_DELETE_KEY_TEST")

    return value is None or value.lower() not in ['true']


# Runs after all tests have finished
def pytest_sessionfinish(session, exitstatus):
    try:
        collections = _client.list_collections()
        for collection in collections:
            collection_id = collection.collection_id

            if collection_id in _protected_collections:
                continue

            _client.delete_collection(collection_id=collection_id)
    except Exception:
        # Do nothing
        pass

    if not CONFIGURATION["other"]["enable_external_api_tests"]:
        return

    try:
        keys = _client.get_external_keys()
        for key in keys:
            _client.delete_external_key(key.external_key_id)
    except Exception:
        # Do nothing
        pass


def random_string(length: int):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@pytest.fixture(scope="module")
def client() -> VantageClient:
    return _client


@pytest.fixture(scope="module")
def random_string_generator() -> Callable:
    return random_string


@pytest.fixture(scope="module")
def random_uuid() -> str:
    return str(uuid.uuid4())


def disable_external_api_keys_tests() -> bool:
    return not CONFIGURATION["other"]["is_mock_api"]
