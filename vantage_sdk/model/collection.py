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
    """User-provided embeddings collection"""

    user_provided_embeddings: StrictBool = True


class VantageManagedEmbeddingsCollection(Collection):
    """Vantage-managed embeddings collection"""

    llm_provider: StrictStr
    user_provided_embeddings: StrictBool = False
    llm_secret: Optional[StrictStr] = None
    external_account_id: Optional[StrictStr] = None

    @model_validator(mode="after")
    def check_extrnal_authentication_method_exists(cls, values):
        if not values.llm_secret and not values.external_account_id:
            raise ValueError(
                "Please provide either `llm_secret` or `external_account_id` to authenticate with the LLM provider."
            )


class OpenAICollection(VantageManagedEmbeddingsCollection):
    """Vantage-managed embeddings collection which uses OpenAI as LLM provider"""

    llm_provider: StrictStr = LLMProvider.OpenAI.value
    llm: StrictStr
    secondary_external_accounts: Optional[
        List[SecondaryExternalAccount]
    ] = None


class HuggingFaceCollection(VantageManagedEmbeddingsCollection):
    """Vantage-managed embeddings collection which uses HuggingFace as LLM provider"""

    llm_provider: StrictStr = LLMProvider.HuggingFace.value
    external_url: StrictStr = None


class CollectionUploadURL(BaseModel):
    collection_id: Optional[StrictStr] = None
    customer_batch_identifier: Optional[StrictStr] = None
    upload_url_type: Optional[StrictStr] = None
    upload_url: Optional[StrictStr] = None
