from typing import Optional, Union

from tests.integration_tests.configuration.loader import CONFIGURATION
from vantage_sdk.client import VantageClient
from vantage_sdk.model.collection import (
    HuggingFaceCollection,
    OpenAICollection,
    UserProvidedEmbeddingsCollection,
)


def create_temporary_upe_collection(
    client: VantageClient,
    collection: UserProvidedEmbeddingsCollection,
    account_id: Optional[str] = None,
) -> Union[
    UserProvidedEmbeddingsCollection,
    OpenAICollection,
    HuggingFaceCollection,
]:
    if CONFIGURATION["other"]["is_mock_api"]:
        return collection

    return client.create_collection(
        account_id=account_id,
        collection=collection,
    )


def create_temporary_collection(
    client: VantageClient,
    collection_id: str,
    collection_name: str,
    user_provided_embeddings: bool,
    embeddings_dimension: int,
    account_id: Optional[str] = None,
) -> Optional[
    Union[
        UserProvidedEmbeddingsCollection,
        OpenAICollection,
        HuggingFaceCollection,
    ]
]:
    if CONFIGURATION["other"]["is_mock_api"]:
        return None

    return client.create_collection(
        account_id=account_id,
        collection_id=collection_id,
        collection_name=collection_name,
        user_provided_embeddings=user_provided_embeddings,
        embeddings_dimension=embeddings_dimension,
    )
