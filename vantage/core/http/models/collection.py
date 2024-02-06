# coding: utf-8

"""
    Vantage API

    This is a the API to interact with Vantage Discovery, the amazing Semantic Search Platform in the world.  We enable developers to build magical discovery experiences into their products and websites.  Some useful links: - [TODO: Semantic Search Guide: What Is It And Why Does It Matter?](https://www.bloomreach.com/en/blog/2019/semantic-search-explained-in-5-minutes)

    The version of the OpenAPI document: v1.1.2
    Contact: devrel@vantagediscovery.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    StrictBool,
    StrictInt,
    StrictStr,
    validator,
)


class Collection(BaseModel):
    """
    Collection
    """

    collection_created_time: Optional[StrictStr] = None
    collection_status: Optional[StrictStr] = None
    collection_state: Optional[StrictStr] = None
    collection_id: Optional[StrictStr] = Field(
        None,
        description="Immutable.  Unique identifier within an account, 3 to 36 characters long with only lower case letters, numeric digits and \"-\"",
    )
    user_provided_embeddings: Optional[StrictBool] = Field(
        False,
        description="Ignore llm field will provide own embeddings for both ingest and search",
    )
    llm: Optional[StrictStr] = None
    embeddings_dimension: Optional[StrictInt] = Field(
        None,
        description="The dimensionality or vector size of the embeddings.  Applies to both user provided embeddings and vantage managed embeddings.",
    )
    external_key_id: Optional[StrictStr] = Field(
        None,
        description="The external API key, for the llm_provider to use for the collection",
    )
    collection_name: Optional[StrictStr] = None
    collection_preview_url_pattern: Optional[StrictStr] = Field(
        None,
        description="To be able to preview items in test on the test collection page, enter in a URL that supports the open graph extensions for previewing links.",
    )
    __properties = [
        "collection_created_time",
        "collection_status",
        "collection_state",
        "collection_id",
        "user_provided_embeddings",
        "llm",
        "embeddings_dimension",
        "external_key_id",
        "collection_name",
        "collection_preview_url_pattern",
    ]

    @validator('collection_status')
    def collection_status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in (
            'Pending',
            'Indexing',
            'Online',
            'Degraded',
            'Offline',
        ):
            raise ValueError(
                "must be one of enum values ('Pending', 'Indexing', 'Online', 'Degraded', 'Offline')"
            )
        return value

    @validator('collection_state')
    def collection_state_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('Active', 'Standby', 'Deleted'):
            raise ValueError(
                "must be one of enum values ('Active', 'Standby', 'Deleted')"
            )
        return value

    class Config:
        """Pydantic configuration"""

        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Collection:
        """Create an instance of Collection from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(
            by_alias=True,
            exclude={
                "collection_created_time",
                "collection_status",
                "collection_state",
            },
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Collection:
        """Create an instance of Collection from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Collection.parse_obj(obj)

        _obj = Collection.parse_obj(
            {
                "collection_created_time": obj.get("collection_created_time"),
                "collection_status": obj.get("collection_status"),
                "collection_state": obj.get("collection_state"),
                "collection_id": obj.get("collection_id"),
                "user_provided_embeddings": obj.get("user_provided_embeddings")
                if obj.get("user_provided_embeddings") is not None
                else False,
                "llm": obj.get("llm"),
                "embeddings_dimension": obj.get("embeddings_dimension"),
                "external_key_id": obj.get("external_key_id"),
                "collection_name": obj.get("collection_name"),
                "collection_preview_url_pattern": obj.get(
                    "collection_preview_url_pattern"
                ),
            }
        )
        return _obj
