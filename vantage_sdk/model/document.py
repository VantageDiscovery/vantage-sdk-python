"""
Models for the Documents API.
"""

import math
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

from vantage_sdk.config import (
    METADATA_ORDERED_PREFIX,
    METADATA_PREFIX,
    UNIT_VECTOR_TOLERANCE,
)


class MetadataItem(BaseModel):
    """
    Represents a metadata item associated with a document.

    Attributes
    ----------
    key : StrictStr
        The key for the metadata item.
    value : Union[StrictStr, StrictInt, StrictFloat, StrictBool]
        The value for the metadata item.
    """

    key: StrictStr
    value: Union[StrictStr, StrictInt, StrictFloat, StrictBool]
    sortable: StrictBool = False

    @model_validator(mode="before")
    def add_prefix(cls, values: Dict):
        key, value, sortable = (
            values.get("key"),
            values.get("value"),
            values.get("sortable"),
        )
        if sortable:
            if not isinstance(value, float):
                raise ValueError(
                    f"Value must be a float if sortable is set to True. Got {value} of type {type(value)}"
                )
            prefix = METADATA_ORDERED_PREFIX
        else:
            prefix = METADATA_PREFIX

        if key:
            values["key"] = prefix + key
        return values


class VariantItem(BaseModel):
    """
    Represents a variant item of a document variant.

    Attributes
    ----------
    key : StrictStr
        The key for the variant item.
    value : Union[StrictStr, StrictInt, StrictFloat, StrictBool]
        The value for the variant item.
    """

    key: StrictStr
    value: Union[StrictStr, StrictInt, StrictFloat, StrictBool]


class Variant(BaseModel):
    """
    Represents a single variant of a document.

    Attributes
    ----------
    id : StrictStr
        Unique ID of variant for this document.
    items : List[VariantItem]
        List of variant items.
    """

    id: StrictStr
    items: List[VariantItem]


class VantageDocument(BaseModel):
    """
    Vantage document class.

    Attributes
    ----------
    id : Optional[StrictStr], optional
        The unique identifier for the document, generated by default if not provided.
    metadata : Optional[List[MetadataItem]], optional
        A list of metadata items associated with the document.
    variants : variants: Optional[List[Variant]], optional
        A list of variant items associated with the document.
    """

    id: Optional[StrictStr] = Field(default_factory=lambda: uuid4().hex)
    metadata: Optional[List[MetadataItem]] = None
    variants: Optional[List[Variant]] = None

    def to_vantage_dict(self):
        vantage_dict = {
            "id": self.id,
        }

        if self.metadata:
            for metadata_item in self.metadata:
                vantage_dict[metadata_item.key] = metadata_item.value
        if self.variants:
            variants_list: List = []
            for variant in self.variants:
                variant_dict: Dict = {"id": variant.id}
                for variant_item in variant.items:
                    variant_dict[variant_item.key] = variant_item.value
                variants_list.append(variant_dict)
            vantage_dict["variants"] = variants_list

        return vantage_dict


class VantageManagedEmbeddingsDocument(VantageDocument):
    """Document class for Vantage-managed embeddings collections"""

    text: StrictStr

    def to_vantage_dict(self):
        vantage_dict = super().to_vantage_dict()
        vantage_dict["text"] = self.text

        return vantage_dict


class UserProvidedEmbeddingsDocument(VantageDocument):
    """Document class for User-provided embeddings collections"""

    embeddings: List[StrictFloat]
    text: Optional[StrictStr] = None

    def to_vantage_dict(self):
        vantage_dict = super().to_vantage_dict()
        vantage_dict["embeddings"] = self.embeddings

        if self.text:
            vantage_dict["text"] = self.text

        return vantage_dict

    @model_validator(mode="before")
    def embedding_vector_unit_vector_validation(cls, cls_values):
        embedding_vector = cls_values.get("embeddings")

        sum_of_squares = sum(x**2 for x in embedding_vector)

        magnitude = math.sqrt(sum_of_squares)

        if not abs(magnitude - 1.0) < UNIT_VECTOR_TOLERANCE:
            raise ValueError('Provided embedding vector is not a unit vector.')

        return cls_values
