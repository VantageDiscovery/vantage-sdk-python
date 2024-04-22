import uuid
from typing import Optional, List, Any, Union, Dict

from pydantic import (
    BaseModel,
    StrictStr,
    StrictFloat,
    StrictBool,
    StrictInt,
    model_validator,
    field_validator,
)

from vantage_sdk.config import METADATA_PREFIX, METADATA_ORDERED_PREFIX


class MetadataItem(BaseModel):
    key: StrictStr
    value: Union[StrictStr, StrictInt, StrictFloat, StrictBool]

    @model_validator(mode="before")
    def add_prefix(cls, values):
        key, value = values.get('key'), values.get('value')
        if isinstance(value, float):
            prefix = METADATA_ORDERED_PREFIX
        else:
            prefix = METADATA_PREFIX

        if key:
            values['key'] = prefix + key
        return values


class VantageDocument(BaseModel):
    text: StrictStr
    metadata: Optional[List[MetadataItem]] = None
    id: Optional[StrictStr] = None

    @field_validator('id', mode="before")
    def set_default_id(cls, v):
        return v or str(uuid.uuid4())

    def to_vantage_dict(self):
        vantage_dict = {
            "id": self.id,
            "text": self.text,
        }

        if self.metadata:
            for metadata_item in self.metadata:
                vantage_dict[metadata_item.key] = metadata_item.value

        return vantage_dict


class VantageManagedEmbeddingsDocument(VantageDocument):
    """Document class for Vantage-managed embeddings collections"""


class UserProvidedEmbeddingsDocument(VantageDocument):
    """Document class for User-provided embeddings collections"""

    embeddings: List[StrictFloat] = None

    def to_vantage_dict(self):
        vantage_dict = super().to_vantage_dict()
        vantage_dict["embeddings"] = self.embeddings

        return vantage_dict
