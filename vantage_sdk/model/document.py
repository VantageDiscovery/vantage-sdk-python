import uuid
from typing import Optional, List, Any, Union, Dict

from pydantic import BaseModel, StrictStr, StrictFloat, StrictBool, StrictInt

from vantage_sdk.config import METADATA_PREFIX, METADATA_ORDERED_PREFIX


class MetadataItem(BaseModel):
    key: StrictStr
    value: Union[StrictStr, StrictInt, StrictFloat, StrictBool]

    def __init__(
        self,
        key: StrictStr,
        value: Union[StrictStr, StrictInt, StrictFloat, StrictBool],
    ) -> None:
        super().__init__(key=key, value=value)
        prefix = (
            METADATA_ORDERED_PREFIX
            if isinstance(value, float)
            else METADATA_PREFIX
        )

        self.key = prefix + key
        self.value = value


class VantageDocument(BaseModel):
    text: StrictStr
    metadata: Optional[List[MetadataItem]] = None
    id: Optional[StrictStr] = None

    def __init__(
        self,
        text: StrictStr,
        metadata: Optional[List[MetadataItem]] = None,
        id: Optional[StrictStr] = None,
    ):
        super().__init__(text=text, metadata=metadata, id=id)
        self.id = id or str(uuid.uuid4())

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

    def __init__(
        self,
        text: StrictStr,
        embeddings: List[StrictFloat],
        metadata: Optional[List[MetadataItem]] = None,
        id: Optional[StrictStr] = None,
    ):
        super().__init__(text=text, metadata=metadata, id=id)
        self.embeddings = embeddings

    def to_vantage_dict(self):
        vantage_dict = super().to_vantage_dict()
        vantage_dict["embeddings"] = self.embeddings

        return vantage_dict
