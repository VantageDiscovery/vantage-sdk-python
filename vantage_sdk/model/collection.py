"""
Models for the Collection API.
"""

from typing import List, Optional

from pydantic import (
    BaseModel,
    StrictBool,
    StrictInt,
    StrictStr,
    model_validator,
)

from vantage_sdk.model.keys import LLMProvider, SecondaryExternalAccount


class Collection(BaseModel):
    """
    A collection of documents.

    Attributes
    ----------
    collection_id: str
        ID of the collection.
    embeddings_dimension: int
        Dimension of embeddings in the collection documents.
    user_provided_embeddings: bool
        If the collection uses user-provided embeddings.
    collection_name: Optional[StrictStr]
        Name of the collection.
    collection_state: Optional[StrictStr]
        Current state of the collection.
    collection_status: Optional[StrictStr]
        Current status of the collection.
    collection_created_time: Optional[StrictStr]
        When the collection was created.
    collection_preview_url_pattern: Optional[StrictStr]
        Preview URL pattern of the collection.
    """

    collection_id: StrictStr
    embeddings_dimension: StrictInt
    user_provided_embeddings: StrictBool
    collection_name: Optional[StrictStr] = None
    collection_state: Optional[StrictStr] = None
    collection_status: Optional[StrictStr] = None
    collection_created_time: Optional[StrictStr] = None
    collection_preview_url_pattern: Optional[StrictStr] = None

    @model_validator(mode="before")
    def set_default_collection_name(cls, values):
        if (
            "collection_name" not in values
            or values["collection_name"] is None
        ):
            collection_id = values.get("collection_id")
            if collection_id:
                values["collection_name"] = f"Collection [{collection_id}]"
        return values


class UserProvidedEmbeddingsCollection(Collection):
    """
    A collection of documents with user-provided embeddings.

    Attributes
    ----------
    user_provided_embeddings : StrictBool
        Indicates that the embeddings in this collection are provided by the user.

    """

    user_provided_embeddings: StrictBool = True


class VantageManagedEmbeddingsCollection(Collection):
    """
    A collection of documents with Vantage-managed embeddings.

    Attributes
    ----------
    user_provided_embeddings : StrictBool
        Indicates that the embeddings in this collection are managed by Vantage.
    llm_provider : StrictStr
        The provider of the embedding model used to generate embeddings.
    llm_secret : Optional[StrictStr], optional
        The secret key used to authenticate with the model provider.
    external_key_id : Optional[StrictStr], optional
        The external key ID used to authenticate with the model provider.
    """

    user_provided_embeddings: StrictBool = False
    llm_provider: StrictStr
    llm_secret: Optional[StrictStr] = None
    external_key_id: Optional[StrictStr] = None

    @model_validator(mode="after")
    def check_extrnal_authentication_method_exists(cls, values):
        if not values.llm_secret and not values.external_key_id:
            raise ValueError(
                "Please provide either `llm_secret` or `external_key_id` to authenticate with the LLM provider."
            )


class OpenAICollection(VantageManagedEmbeddingsCollection):
    """
    Vantage-managed embeddings collection which uses OpenAI as LLM provider.

    Attributes
    ----------
    llm_provider : StrictStr
        The provider of the embedding model, set to OpenAI.
    llm : StrictStr
        The specific embedding model used from OpenAI.
    secondary_external_accounts : Optional[List[SecondaryExternalAccount]], optional
        A list of secondary external accounts associated with the collection.
    """

    llm_provider: StrictStr = LLMProvider.OpenAI.value
    llm: StrictStr
    secondary_external_accounts: Optional[
        List[SecondaryExternalAccount]
    ] = None


class HuggingFaceCollection(VantageManagedEmbeddingsCollection):
    """
    Vantage-managed embeddings collection which uses HuggingFace as LLM provider.

    Attributes
    ----------
    llm_provider : StrictStr
        The provider of the embedding model, set to HuggingFace.
    external_url : StrictStr
        The external URL for the HuggingFace model.
    """

    llm_provider: StrictStr = LLMProvider.HuggingFace.value
    external_url: StrictStr = None


class CollectionUploadURL(BaseModel):
    """
    Represents the upload URL details for a collection.

    Attributes
    ----------
    collection_id : Optional[StrictStr], optional
        The unique identifier for the collection.
    customer_batch_identifier : Optional[StrictStr], optional
        The identifier for the customer batch.
    upload_url_type : Optional[StrictStr], optional
        The type of the upload URL.
    upload_url : Optional[StrictStr], optional
        The URL used for uploading to the collection.
    """

    collection_id: Optional[StrictStr] = None
    customer_batch_identifier: Optional[StrictStr] = None
    upload_url_type: Optional[StrictStr] = None
    upload_url: Optional[StrictStr] = None
