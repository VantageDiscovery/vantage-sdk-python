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

from pydantic import BaseModel, Field, StrictStr, validator


class ExternalAPIKey(BaseModel):
    """
    ExternalAPIKey
    """

    external_key_id: Optional[StrictStr] = Field(
        None, description="The unique id of the key"
    )
    account_id: Optional[StrictStr] = Field(
        None, description="The account this key is contained within"
    )
    external_key_created_date: Optional[StrictStr] = Field(
        None, description="date this key was created"
    )
    url: Optional[StrictStr] = None
    llm_provider: Optional[StrictStr] = None
    llm_secret: Optional[StrictStr] = None
    __properties = [
        "external_key_id",
        "account_id",
        "external_key_created_date",
        "url",
        "llm_provider",
        "llm_secret",
    ]

    @validator('llm_provider')
    def llm_provider_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('OpenAI', 'HuggingFace'):
            raise ValueError(
                "must be one of enum values ('OpenAI', 'HuggingFace')"
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
    def from_json(cls, json_str: str) -> ExternalAPIKey:
        """Create an instance of ExternalAPIKey from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(
            by_alias=True,
            exclude={
                "external_key_id",
                "account_id",
                "external_key_created_date",
            },
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ExternalAPIKey:
        """Create an instance of ExternalAPIKey from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ExternalAPIKey.parse_obj(obj)

        _obj = ExternalAPIKey.parse_obj(
            {
                "external_key_id": obj.get("external_key_id"),
                "account_id": obj.get("account_id"),
                "external_key_created_date": obj.get(
                    "external_key_created_date"
                ),
                "url": obj.get("url"),
                "llm_provider": obj.get("llm_provider"),
                "llm_secret": obj.get("llm_secret"),
            }
        )
        return _obj
