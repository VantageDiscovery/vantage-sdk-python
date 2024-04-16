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

from pydantic import BaseModel, Field, StrictStr

from vantage_sdk.core.http.models.collection_modifiable_secondary_external_accounts_inner import (
    CollectionModifiableSecondaryExternalAccountsInner,
)


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class CollectionModifiable(BaseModel):
    """
    CollectionModifiable
    """  # noqa: E501

    external_key_id: Optional[StrictStr] = Field(
        default=None,
        description="The external API key, for the llm_provider to use for the collection",
    )
    secondary_external_accounts: Optional[
        List[CollectionModifiableSecondaryExternalAccountsInner]
    ] = None
    collection_name: Optional[StrictStr] = None
    collection_preview_url_pattern: Optional[StrictStr] = Field(
        default=None,
        description="To be able to preview items in test on the test collection page, enter in a URL that supports the open graph extensions for previewing links.",
    )
    __properties: ClassVar[List[str]] = [
        "external_key_id",
        "secondary_external_accounts",
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
        """Create an instance of CollectionModifiable from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in secondary_external_accounts (list)
        _items = []
        if self.secondary_external_accounts:
            for _item in self.secondary_external_accounts:
                if _item:
                    _items.append(_item.to_dict())
            _dict['secondary_external_accounts'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of CollectionModifiable from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "external_key_id": obj.get("external_key_id"),
                "secondary_external_accounts": [
                    CollectionModifiableSecondaryExternalAccountsInner.from_dict(
                        _item
                    )
                    for _item in obj.get("secondary_external_accounts")
                ]
                if obj.get("secondary_external_accounts") is not None
                else None,
                "collection_name": obj.get("collection_name"),
                "collection_preview_url_pattern": obj.get(
                    "collection_preview_url_pattern"
                ),
            }
        )
        return _obj
