import os
import random
import string
import uuid
from typing import Callable, List

import pytest

from vantage_sdk.client import VantageClient
from vantage_sdk.exceptions import VantageNotFoundError
from vantage_sdk.model.document import (
    UserProvidedEmbeddingsDocument,
    VantageManagedEmbeddingsDocument,
)


ABS_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(ABS_PATH, os.pardir, os.pardir))
DISABLE_EXTERNAL_API_KEYS_TESTS = True


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
        "more_like_this_collection": os.getenv(
            "VANTAGE_MORE_LIKE_THIS_SEARCH_COLLECTION_ID"
        ),
    },
    "keys": {
        "vantage_api_key": os.getenv("VANTAGE_API_KEY"),
        "vantage_api_key_id": os.getenv("VANTAGE_API_KEY_ID"),
        "open_api_key": os.getenv("OPEN_API_KEY"),
        "open_api_key_id": os.getenv("OPEN_API_KEY_ID"),
        "external_api_key": os.getenv("EXTERNAL_API_KEY"),
        "external_api_key_id": os.getenv("EXTERNAL_API_KEY_ID"),
        "external_api_key_provider": os.getenv("EXTERNAL_API_KEY_PROVIDER"),
    },
}

auth_method = os.getenv("VANTAGE_AUTH_METHOD", "client_credentials")
jwt_token = os.getenv("VANTAGE_API_JWT_TOKEN", None)

if auth_method == "api_key":
    api_key = _configuration["keys"]["vantage_api_key"]

    if api_key is None:
        raise ValueError("Vantage API key unspecified.")

    _client = VantageClient.using_vantage_api_key(
        vantage_api_key=api_key,
        account_id=_configuration["account"]["id"],
        api_host=_configuration["api"]["api_host"],
    )
elif auth_method == "jwt_token":
    if jwt_token is None:
        raise ValueError("JWT token unspecified.")

    _client = VantageClient.using_jwt_token(
        vantage_api_jwt_token=jwt_token,
        account_id=_configuration["account"]["id"],
        api_host=_configuration["api"]["api_host"],
    )
elif auth_method == "client_credentials":
    client_id = _configuration["api"]["client_id"]
    client_secret = _configuration["api"]["client_secret"]

    if client_id is None or client_secret is None:
        raise ValueError("Missing client credentials.")

    _client = VantageClient.using_client_credentials(
        vantage_client_id=_configuration["api"]["client_id"],
        vantage_client_secret=_configuration["api"]["client_secret"],
        api_host=_configuration["api"]["api_host"],
        auth_host=_configuration["api"]["auth_host"],
        account_id=_configuration["account"]["id"],
    )
else:
    raise ValueError(
        f"Unknown auth method in $VANTAGE_AUTH_METHOD: {auth_method}"
    )

_protected_collections = []

embedding_collection_id = _configuration["collection"].get(
    "embedding_search_test_collection_id"
)
semantic_colection_id = _configuration["collection"].get(
    "semantic_search_test_collection_id"
)
mlt_collection_id = _configuration["collection"].get(
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
    except VantageNotFoundError:
        # Do nothing
        pass

    if DISABLE_EXTERNAL_API_KEYS_TESTS:
        return

    try:
        keys = _client.get_external_api_keys()
        for key in keys:
            _client.delete_external_api_key(key.external_key_id)
    except VantageNotFoundError:
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
    vantage_api_key = _configuration["keys"].get("vantage_api_key")
    if vantage_api_key is None:
        pytest.skip("No Vantage API key available.")

    return vantage_api_key


@pytest.fixture(scope="module")
def vantage_api_key_id() -> dict:
    vantage_api_key_id = _configuration["keys"].get("vantage_api_key_id")
    if vantage_api_key_id is None:
        pytest.skip("No Vantage API key ID available.")

    return vantage_api_key_id


@pytest.fixture(scope="module")
def open_api_key() -> str:
    open_api_key = _configuration["keys"].get("open_api_key")
    if open_api_key is None:
        pytest.skip("No OpenAPI key available.")

    return open_api_key


@pytest.fixture(scope="module")
def external_api_key() -> str:
    external_api_key = _configuration["keys"].get("external_api_key")
    if external_api_key is None:
        pytest.skip("No external API key available.")

    return external_api_key


@pytest.fixture(scope="module")
def external_api_key_id() -> str:
    external_api_key_id = _configuration["keys"].get("external_api_key_id")
    if external_api_key_id is None:
        pytest.skip("No external API key ID available.")

    return external_api_key_id


@pytest.fixture(scope="module")
def external_api_key_provider() -> str:
    external_api_key_provider = _configuration["keys"][
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
def more_like_this_test_collection_id() -> str:
    mlt_search_test_collection_id = _configuration["collection"].get(
        "more_like_this_collection"
    )

    if mlt_search_test_collection_id is None:
        pytest.skip("No more like this search test collection available.")

    return mlt_search_test_collection_id


@pytest.fixture(scope="module")
def embedding_search_test_collection_id_for_setup() -> str:
    embedding_search_test_collection_id = _configuration["collection"].get(
        "embedding_search_test_collection_id"
    )

    if embedding_search_test_collection_id is None:
        pytest.skip("No embedding search test collection available.")

    return embedding_search_test_collection_id


@pytest.fixture(scope="module")
def semantic_search_test_collection_id_for_setup() -> str:
    semantic_search_test_collection_id = _configuration["collection"].get(
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
