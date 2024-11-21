from typing import List

import pytest

from vantage_sdk.model.document import (
    MetadataItem,
    UserProvidedEmbeddingsDocument,
    VantageManagedEmbeddingsDocument,
    Variant,
    VariantItem,
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
    metadata = [
        [MetadataItem(key="test_1", value="1")],
        [MetadataItem(key="test_2", value="2")],
        [MetadataItem(key="test_3", value="3")],
        [MetadataItem(key="test_4", value="4")],
    ]
    variants = [
        [Variant(id="v1", items=[VariantItem(key="color", value="red")])],
        [Variant(id="v2", items=[VariantItem(key="color", value="green")])],
        [Variant(id="v3", items=[VariantItem(key="color", value="blue")])],
        [Variant(id="v4", items=[VariantItem(key="color", value="purple")])],
    ]
    documents = [
        UserProvidedEmbeddingsDocument(
            text=text,
            id=id,
            embeddings=emb,
            metadata=meta,
            variants=var,
        )
        for id, text, emb, meta, var in zip(
            ids,
            texts,
            embeddings,
            metadata,
            variants,
        )
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
    metadata = [
        [MetadataItem(key="test_1", value="1")],
        [MetadataItem(key="test_2", value="2")],
        [MetadataItem(key="test_3", value="3")],
        [MetadataItem(key="test_4", value="4")],
    ]
    variants = [
        [Variant(id="v1", items=[VariantItem(key="color", value="red")])],
        [Variant(id="v2", items=[VariantItem(key="color", value="green")])],
        [Variant(id="v3", items=[VariantItem(key="color", value="blue")])],
        [Variant(id="v4", items=[VariantItem(key="color", value="purple")])],
    ]

    documents = [
        VantageManagedEmbeddingsDocument(
            text=text, id=id, metadata=meta, variants=var
        )
        for id, text, meta, var in zip(
            ids,
            texts,
            metadata,
            variants,
        )
    ]

    return documents
