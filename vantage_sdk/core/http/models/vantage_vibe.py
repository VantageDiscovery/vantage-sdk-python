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

from pydantic import BaseModel, StrictStr


try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class VantageVibe(BaseModel):
    """
    VantageVibe
    """  # noqa: E501

    id: Optional[StrictStr] = None
    account_id: Optional[StrictStr] = None
    llm_model_name: Optional[StrictStr] = None
    name: Optional[StrictStr] = None
    external_account_id: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = [
        "id",
        "account_id",
        "llm_model_name",
        "name",
        "external_account_id",
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
        """Create an instance of VantageVibe from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
                "id",
                "account_id",
            },
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of VantageVibe from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "id": obj.get("id"),
                "account_id": obj.get("account_id"),
                "llm_model_name": obj.get("llm_model_name"),
                "name": obj.get("name"),
                "external_account_id": obj.get("external_account_id"),
            }
        )
        return _obj
