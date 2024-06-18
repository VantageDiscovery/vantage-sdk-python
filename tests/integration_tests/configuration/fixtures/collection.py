import os

import pytest

from tests.integration_tests.configuration.loader import CONFIGURATION
from tests.integration_tests.configuration.mock_api import (
    get_mock_request_for,
    get_request_stub_file_contents,
)


use_mock_api = CONFIGURATION["other"]["is_mock_api"]


def _get_collection_id_for_mock_api(request) -> str:
    """Get collection names directly from wiremock stub files."""
    module_name = os.path.basename(request.path).replace(".py", "")
    test_name = request.node.name

    if test_name in (
        "test_documents_upload_from_parquet_file",
        "test_documents_upload_from_jsonl_file",
    ):
        stub = get_mock_request_for(
            module_name="test_documents",
            test_name="test_documents_upload_from_parquet_file-upload_url",
        )
    else:
        stub = get_request_stub_file_contents(request)

    if module_name == "test_search":
        return stub["request"]["urlPath"].split("/")[4]

    if test_name in (
        "test_create_collection_with_user_embeddings",
        "test_create_vantage_managed_embeddings_collection",
    ):
        return stub["response"]["jsonBody"]["collection_id"]

    urlPart = None
    if "url" in stub["request"]:
        urlPart = stub["request"]["url"]
    else:
        urlPart = stub["request"]["urlPath"]

    return urlPart.split("/")[5]


def _get_collection_id_for_real_api(request) -> str:
    collection = CONFIGURATION["collection"]
    test_name = request.node.name

    if test_name in (
        "test_upload_user_embeddings_to_a_non_existing_collection",
        "test_get_non_existing_collection",
        "test_update_non_existing_collection",
        "test_delete_non_existing_collection",
        "test_embedding_search_on_non_existing_collection",
        "test_semantic_search_on_non_existing_collection",
    ):
        return collection["non_existing_collection_id"]

    if test_name == "test_update_collection":
        return collection["collection_to_update_id"]

    if test_name == "test_delete_collection":
        return collection["collection_to_delete_id"]

    if test_name == "test_if_embedding_search_returns_result":
        return collection["embedding_search_test_collection_id"]

    if test_name == "test_if_semantic_search_returns_result":
        return collection["semantic_search_test_collection_id"]

    return collection["collection_id"]


@pytest.fixture(scope="module")
def collection_params() -> dict:
    return CONFIGURATION["collection"]


@pytest.fixture(scope="function")
def test_collection_id(request) -> str:
    if not use_mock_api:
        return CONFIGURATION["collection"]["id"]

    return _get_collection_id_for_mock_api(request)
