from typing import Optional

from pydantic import BaseModel, StrictBool, StrictInt, StrictStr


class Collection(BaseModel):
    created_time: Optional[StrictStr] = None
    status: Optional[StrictStr] = None
    state: Optional[StrictStr] = None
    id: Optional[StrictStr] = None
    user_provided_embeddings: Optional[StrictBool] = None
    llm: Optional[StrictStr] = None
    embeddings_dimension: Optional[StrictInt] = None
    external_key_id: Optional[StrictStr] = None
    name: Optional[StrictStr] = None
    preview_url_pattern: Optional[StrictStr] = None


class CollectionUploadURL(BaseModel):
    collection_id: Optional[StrictStr] = None
    customer_batch_identifier: Optional[StrictStr] = None
    upload_url_type: Optional[StrictStr] = None
    upload_url: Optional[StrictStr] = None
