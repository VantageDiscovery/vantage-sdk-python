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
from typing import Any, ClassVar, Dict, List, Optional

from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class CreateCollectionRequest(BaseModel):
    """
    CreateCollectionRequest
    """  # noqa: E501

    collection_id: StrictStr = Field(
        description="Immutable.  Unique identifier within an account, 3 to 36 characters long with only lower case letters, numeric digits and \"-\""
    )
    user_provided_embeddings: Optional[StrictBool] = Field(
        default=False,
        description="Ignore llm field will provide own embeddings for both ingest and search",
    )
    llm: Optional[StrictStr] = None
    embeddings_dimension: StrictInt = Field(
        description="The dimensionality or vector size of the embeddings.  Applies to both user provided embeddings and vantage managed embeddings."
    )
    external_account_id: Optional[StrictStr] = Field(
        default=None,
        description="The external API key, for the llm_provider to use for the collection",
    )
    collection_name: StrictStr
    collection_preview_url_pattern: Optional[StrictStr] = Field(
        default=None,
        description="To be able to preview items in test on the test collection page, enter in a URL that supports the open graph extensions for previewing links.",
    )
    __properties: ClassVar[List[str]] = [
        "collection_id",
        "user_provided_embeddings",
        "llm",
        "embeddings_dimension",
        "external_account_id",
        "collection_name",
        "collection_preview_url_pattern",
    ]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of CreateCollectionRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={},
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of CreateCollectionRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "collection_id": obj.get("collection_id"),
                "user_provided_embeddings": obj.get("user_provided_embeddings")
                if obj.get("user_provided_embeddings") is not None
                else False,
                "llm": obj.get("llm"),
                "embeddings_dimension": obj.get("embeddings_dimension"),
                "external_account_id": obj.get("external_account_id"),
                "collection_name": obj.get("collection_name"),
                "collection_preview_url_pattern": obj.get(
                    "collection_preview_url_pattern"
                ),
            }
        )
        return _obj
