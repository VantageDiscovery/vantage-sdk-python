from typing import Dict, List, Optional, Union
from uuid import uuid4

from pydantic import (
    BaseModel,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    model_validator,
)

from vantage_sdk.config import METADATA_ORDERED_PREFIX, METADATA_PREFIX


class MetadataItem(BaseModel):
    key: StrictStr
    value: Union[StrictStr, StrictInt, StrictFloat, StrictBool]

    @model_validator(mode="before")
    def add_prefix(cls, values: Dict):
        key, value = values.get("key"), values.get("value")
        if isinstance(value, float):
            prefix = METADATA_ORDERED_PREFIX
        else:
            prefix = METADATA_PREFIX

        if key:
            values["key"] = prefix + key
        return values


class VantageDocument(BaseModel):
    text: StrictStr
    id: Optional[StrictStr] = Field(default_factory=lambda: uuid4().hex)
    metadata: Optional[List[MetadataItem]] = None

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

    embeddings: List[StrictFloat]

    def to_vantage_dict(self):
        vantage_dict = super().to_vantage_dict()
        vantage_dict["embeddings"] = self.embeddings

        return vantage_dict
