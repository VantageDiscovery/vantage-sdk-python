from typing import List

import pytest

from vantage_sdk.model.document import (
    UserProvidedEmbeddingsDocument,
    VantageManagedEmbeddingsDocument,
)


@pytest.fixture(scope="module")
def jsonl_documents_path() -> str:
    return "tests/data/small_documents.jsonl"


@pytest.fixture(scope="module")
def parquet_file_path() -> str:
    return "tests/data/hello_world.parquet"


@pytest.fixture(scope="module")
def test_parquet_file_path() -> str:
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
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
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
