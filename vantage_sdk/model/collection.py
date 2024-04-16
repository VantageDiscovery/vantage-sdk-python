from typing import Optional, List

from pydantic import BaseModel, StrictBool, StrictInt, StrictStr

from vantage_sdk.model.keys import SecondaryExternalAccount


class Collection(BaseModel):
    collection_created_time: Optional[StrictStr] = None
    collection_status: Optional[StrictStr] = None
    collection_state: Optional[StrictStr] = None
    collection_id: Optional[StrictStr] = None
    user_provided_embeddings: Optional[StrictBool] = None
    llm: Optional[StrictStr] = None
    external_url: Optional[StrictStr] = None
    embeddings_dimension: Optional[StrictInt] = None
    external_account_id: Optional[StrictStr] = None
    secondary_external_accounts: Optional[List[SecondaryExternalAccount]] = (
        None
    )
    collection_name: Optional[StrictStr] = None
    collection_preview_url_pattern: Optional[StrictStr] = None


class CollectionUploadURL(BaseModel):
    collection_id: Optional[StrictStr] = None
    customer_batch_identifier: Optional[StrictStr] = None
    upload_url_type: Optional[StrictStr] = None
    upload_url: Optional[StrictStr] = None
