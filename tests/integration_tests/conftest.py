import os
import random
import string
from typing import Callable

import pytest

from vantage.exceptions import VantageNotFoundException
from vantage.vantage import Vantage


ABS_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(ABS_PATH, os.pardir, os.pardir))


def _load_env() -> None:
    dotenv_path = os.path.join(
        PROJECT_DIR, "tests", "integration_tests", ".env"
    )
    if os.path.exists(dotenv_path):
        from dotenv import load_dotenv

        load_dotenv(dotenv_path)


_load_env()

_configuration = {
    "api": {
        "client_id": os.getenv("VANTAGE_CLIENT_ID"),
        "client_secret": os.getenv("VANTAGE_CLIENT_SECRET"),
        "auth_host": os.getenv("VANTAGE_AUTH_HOST"),
        "api_host": os.getenv("VANTAGE_API_HOST"),
    },
    "account": {
        "id": os.getenv("TEST_ACCOUNT_ID"),
        "name": os.getenv("TEST_ACCOUNT_NAME"),
    },
    "collection": {
        "embedding_search_test_collection_id": os.getenv(
            "VANTAGE_EMBEDDING_SEARCH_TEST_COLLECTION_ID"
        ),
        "semantic_search_test_collection_id": os.getenv(
            "VANTAGE_SEMANTIC_SEARCH_TEST_COLLECTION_ID"
        ),
    },
    "keys": {
        "vantage_api_key": os.getenv("VANTAGE_API_KEY"),
        "open_api_key": os.getenv("OPEN_API_KEY"),
    },
}

jwt_token = os.getenv("VANTAGE_API_JWT_TOKEN")

if jwt_token:
    _client = Vantage.using_jwt_token(
        vantage_api_jwt_token=jwt_token,
        account_id=_configuration["account"]["id"],
        api_host=_configuration["api"]["api_host"],
    )
else:
    _client = Vantage.using_client_credentials(
        vantage_client_id=_configuration["api"]["client_id"],
        vantage_client_secret=_configuration["api"]["client_secret"],
        api_host=_configuration["api"]["api_host"],
        auth_host=_configuration["api"]["auth_host"],
        account_id=_configuration["account"]["id"],
    )

_protected_collections = []

embedding_collection_id = _configuration["collection"][
    "embedding_search_test_collection_id"
]
semantic_colection_id = _configuration["collection"][
    "semantic_search_test_collection_id"
]
if embedding_collection_id:
    _protected_collections.append(embedding_collection_id)
if semantic_colection_id:
    _protected_collections.append(semantic_colection_id)


# Runs after all tests have finished
def pytest_sessionfinish(session, exitstatus):
    account_id = _configuration["account"]["id"]
    try:
        collections = _client.list_collections(account_id=account_id)
        for collection in collections:
            collection_id = collection.actual_instance.collection_id

            if collection_id in _protected_collections:
                continue

            _client.delete_collection(
                collection_id=collection_id,
                account_id=account_id,
            )
    except VantageNotFoundException:
        # Do nothing
        pass


def _random_string(length: int):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@pytest.fixture(scope="module")
def api_params() -> dict:
    return _configuration["api"]


@pytest.fixture(scope="module")
def account_params() -> dict:
    return _configuration["account"]


@pytest.fixture(scope="module")
def collection_params() -> dict:
    return _configuration["collection"]


@pytest.fixture(scope="module")
def vantage_api_key() -> dict:
    vantage_api_key = _configuration["keys"]["vantage_api_key"]
    if vantage_api_key is None:
        pytest.skip("No Vantage API key key available.")

    return vantage_api_key


@pytest.fixture(scope="module")
def open_api_key() -> str:
    open_api_key = _configuration["keys"]["open_api_key"]
    if open_api_key is None:
        pytest.skip("No OpenAPI key available.")

    return open_api_key


@pytest.fixture(scope="module")
def client() -> Vantage:
    return _client


@pytest.fixture(scope="module")
def random_string_generator() -> Callable:
    return _random_string


@pytest.fixture(scope="module")
def test_parquet_file_path() -> str:
    return "tests/data/hello_world.parquet"


@pytest.fixture(scope="module")
def embedding_search_test_collection_id() -> str:
    embedding_search_test_collection_id = _configuration["collection"][
        "embedding_search_test_collection_id"
    ]

    if embedding_search_test_collection_id is None:
        pytest.skip("No embedding search test collection available.")

    return embedding_search_test_collection_id


@pytest.fixture(scope="module")
def semantic_search_test_collection_id() -> str:
    semantic_search_test_collection_id = _configuration["collection"][
        "semantic_search_test_collection_id"
    ]

    if semantic_search_test_collection_id is None:
        pytest.skip("No semantic search test collection available.")

    return semantic_search_test_collection_id


@pytest.fixture(scope="module")
def embedding_search_test_collection_id_for_setup() -> str:
    return _configuration["collection"]["embedding_search_test_collection_id"]


@pytest.fixture(scope="module")
def semantic_search_test_collection_id_for_setup() -> str:
    return _configuration["collection"]["semantic_search_test_collection_id"]
