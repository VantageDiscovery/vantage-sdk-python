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
from typing import Any, ClassVar, Dict, List, Optional, Union

from pydantic import BaseModel, StrictFloat, StrictInt, StrictStr

from vantage_sdk.core.http.models.variant_result import VariantResult


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class SearchResultValues(BaseModel):
    """
    SearchResultValues
    """  # noqa: E501

    id: Optional[StrictStr] = None
    score: Optional[Union[StrictFloat, StrictInt]] = None
    sort_score: Optional[Union[StrictFloat, StrictInt]] = None
    variants: Optional[List[VariantResult]] = None
    variants_full_list: Optional[List[VariantResult]] = None
    fields: Optional[Dict[str, Any]] = None
    __properties: ClassVar[List[str]] = [
        "id",
        "score",
        "sort_score",
        "variants",
        "variants_full_list",
        "fields",
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
        """Create an instance of SearchResultValues from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in variants (list)
        _items = []
        if self.variants:
            for _item in self.variants:
                if _item:
                    _items.append(_item.to_dict())
            _dict['variants'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in variants_full_list (list)
        _items = []
        if self.variants_full_list:
            for _item in self.variants_full_list:
                if _item:
                    _items.append(_item.to_dict())
            _dict['variants_full_list'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of SearchResultValues from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "id": obj.get("id"),
                "score": obj.get("score"),
                "sort_score": obj.get("sort_score"),
                "variants": [
                    VariantResult.from_dict(_item)
                    for _item in obj.get("variants")
                ]
                if obj.get("variants") is not None
                else None,
                "variants_full_list": [
                    VariantResult.from_dict(_item)
                    for _item in obj.get("variants_full_list")
                ]
                if obj.get("variants_full_list") is not None
                else None,
                "fields": obj.get("fields"),
            }
        )
        return _obj
