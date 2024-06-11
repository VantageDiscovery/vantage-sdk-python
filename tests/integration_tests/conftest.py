import os
import random
import string
import uuid
from typing import Callable, List

import pytest

from tests.integration_tests.configuration.client import create_client
from tests.integration_tests.configuration.loader import CONFIGURATION
from vantage_sdk.client import VantageClient
from vantage_sdk.model.document import (
    UserProvidedEmbeddingsDocument,
    VantageManagedEmbeddingsDocument,
)


# Import fixtures
pytest_plugins = [
    "tests.integration_tests.configuration.fixtures.account",
]

use_mock_api = True if os.getenv("USE_MOCK_API", "false") == "true" else False

if use_mock_api:
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
# def pytest_sessionfinish(session, exitstatus):
#     try:
#         collections = _client.list_collections()
#         for collection in collections:
#             collection_id = collection.collection_id

#             if collection_id in _protected_collections:
#                 continue

#             _client.delete_collection(collection_id=collection_id)
#     except VantageNotFoundError:
#         # Do nothing
#         pass

#     if DISABLE_EXTERNAL_API_KEYS_TESTS:
#         return

#     try:
#         keys = _client.get_external_api_keys()
#         for key in keys:
#             _client.delete_external_api_key(key.external_key_id)
#     except VantageNotFoundError:
#         # Do nothing
#         pass


def random_string(length: int):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@pytest.fixture(scope="module")
def api_params() -> dict:
    return CONFIGURATION["api"]


@pytest.fixture(scope="module")
def account_params() -> dict:
    return CONFIGURATION["account"]


@pytest.fixture(scope="module")
def collection_params() -> dict:
    return CONFIGURATION["collection"]


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


@pytest.fixture(scope="module")
def client() -> VantageClient:
    return _client


@pytest.fixture(scope="module")
def random_string_generator() -> Callable:
    return random_string


@pytest.fixture(scope="module")
def test_parquet_file_path() -> str:
    return "tests/data/hello_world.parquet"


@pytest.fixture(scope="module")
def embedding_search_test_collection_id() -> str:
    embedding_search_test_collection_id = CONFIGURATION["collection"][
        "embedding_search_test_collection_id"
    ]

    if embedding_search_test_collection_id is None:
        pytest.skip("No embedding search test collection available.")

    return embedding_search_test_collection_id


@pytest.fixture(scope="module")
def semantic_search_test_collection_id() -> str:
    semantic_search_test_collection_id = CONFIGURATION["collection"][
        "semantic_search_test_collection_id"
    ]

    if semantic_search_test_collection_id is None:
        pytest.skip("No semantic search test collection available.")

    return semantic_search_test_collection_id


@pytest.fixture(scope="module")
def more_like_this_test_collection_id() -> str:
    mlt_search_test_collection_id = CONFIGURATION["collection"].get(
        "more_like_this_collection"
    )

    if mlt_search_test_collection_id is None:
        pytest.skip("No more like this search test collection available.")

    return mlt_search_test_collection_id


@pytest.fixture(scope="module")
def embedding_search_test_collection_id_for_setup() -> str:
    embedding_search_test_collection_id = CONFIGURATION["collection"].get(
        "embedding_search_test_collection_id"
    )

    if embedding_search_test_collection_id is None:
        pytest.skip("No embedding search test collection available.")

    return embedding_search_test_collection_id


@pytest.fixture(scope="module")
def semantic_search_test_collection_id_for_setup() -> str:
    semantic_search_test_collection_id = CONFIGURATION["collection"].get(
        "semantic_search_test_collection_id"
    )

    if semantic_search_test_collection_id is None:
        pytest.skip("No embedding search test collection available.")

    return semantic_search_test_collection_id


@pytest.fixture(scope="module")
def random_uuid() -> str:
    return str(uuid.uuid4())


@pytest.fixture(scope="module")
def jsonl_documents_path() -> str:
    return "tests/data/documents.jsonl"


@pytest.fixture(scope="module")
def parquet_file_path() -> str:
    return "tests/data/hello_world.parquet"


@pytest.fixture(scope="module")
def vantage_upe_documents() -> List[UserProvidedEmbeddingsDocument]:
    ids = [
        "1",
        "2",
        "3",
        "4",
    ]

    texts = [
        "First text",
        "Second text",
        "Third text",
        "Fourth text",
    ]

    embeddings = [
        [0.123, 0.234, 0.345],
        [0.456, 0.567, 0.678],
        [0.789, 0.891, 0.912],
        [0.257, 0.389, 0.468],
    ]
    documents = [
        UserProvidedEmbeddingsDocument(text=text, id=id, embeddings=emb)
        for id, text, emb in zip(ids, texts, embeddings)
    ]

    return documents


@pytest.fixture(scope="module")
def vantage_vme_documents() -> List[VantageManagedEmbeddingsDocument]:
    ids = [
        "1",
        "2",
        "3",
        "4",
    ]

    texts = [
        "First text",
        "Second text",
        "Third text",
        "Fourth text",
    ]

    documents = [
        VantageManagedEmbeddingsDocument(text=text, id=id)
        for id, text in zip(ids, texts)
    ]

    return documents
