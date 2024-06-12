import pytest

from tests.integration_tests.configuration.loader import CONFIGURATION


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
